import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http'; // Import HttpClient for API requests
import { environment } from '../../environments/environment';

interface QuizItem {
  type: string;
  question: string;
  options?: string[];
  selectedOption?: string;
  userResponse?: string; // For storing the user's short response answer
  correctAnswer?: string;
  isCorrect?: boolean;
  explanation?: string;
  gradingResult?: string; // To store the result for short response grading
}

@Component({
  selector: 'app-question-display',
  standalone: true,
  templateUrl: './question-display.component.html',
  styleUrls: ['./question-display.component.css'],
  imports: [CommonModule, FormsModule],
})
export class QuestionDisplayComponent implements OnInit {
  quiz: QuizItem[] | null = null;
  topic: string | null = null;
  isSubmitted: boolean = false;
  apiUrl = environment.apiUrl

  constructor(private router: Router, private http: HttpClient) { // Inject HttpClient
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras?.state) {
      this.quiz = navigation.extras?.state?.['quiz'] || null;
      this.topic = navigation.extras?.state?.['topic'] || 'Quiz';
      this.topic = this.topic ? this.capitalizeFirstLetter(this.topic) : null;
    }
  }

  capitalizeFirstLetter(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  ngOnInit(): void { }

  submitQuiz(): void {
    this.isSubmitted = true;
    if (this.quiz) {
      this.quiz.forEach((item) => {
        if (item.type === 'multiple_choice') {
          item.isCorrect = item.selectedOption === item.correctAnswer;
        } else if (item.type === 'short_response') {
          this.gradeShortResponse(item); // Grade short response questions
        }
      });
    }
    console.log('Submitted Quiz:', this.quiz);
  }

  selectAnswer(questionIndex: number, answer: string): void {
    if (this.quiz && !this.isSubmitted) {
      this.quiz[questionIndex].selectedOption = answer;
    }
  }

  getAnswerClass(questionIndex: number, answer: string): string {
    if (!this.isSubmitted) return '';

    const question = this.quiz ? this.quiz[questionIndex] : null;
    if (!question) return '';

    if (answer === question.correctAnswer) {
      return 'correct';
    } else if (answer === question.selectedOption) {
      return 'incorrect';
    }
    return '';
  }

  gradeShortResponse(item: QuizItem): void {
    const payload = {
      user_response: item.userResponse || '',
      correct_answer: item.correctAnswer || ''
    };

    this.http.post<any>(`${this.apiUrl}/grade-short-response`, payload).subscribe(response => {
      item.gradingResult = response.result;
    });
  }
}
