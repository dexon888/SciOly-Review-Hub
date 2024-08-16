import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';  // Import FormsModule for two-way binding

// Define the QuizItem interface if it's not defined elsewhere
interface QuizItem {
  type: string;
  question: string;
  options?: string[];  // Array of options for multiple-choice questions
  selectedOption?: string;  // To store the selected answer
  correctAnswer?: string;  // The correct answer for the question
  isCorrect?: boolean;  // To indicate if the selected answer is correct
  explanationRequired?: boolean;  // Flag if explanation is needed
  explanation?: string;  // For storing the user's explanation
  answer?: string;  // For short response questions
}

@Component({
  selector: 'app-question-display',
  standalone: true,
  templateUrl: './question-display.component.html',
  styleUrls: ['./question-display.component.css'],
  imports: [CommonModule, FormsModule]  // Ensure FormsModule is included
})
export class QuestionDisplayComponent implements OnInit {
  quiz: QuizItem[] | null = null;
  topic: string | null = null;
  isSubmitted: boolean = false;

  constructor(private router: Router) {
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

  ngOnInit(): void {}

  submitQuiz(): void {
    this.isSubmitted = true;
    if (this.quiz) {
      this.quiz.forEach((item) => {
        if (item.type === 'multiple_choice') {
          item.isCorrect = item.selectedOption === item.correctAnswer;
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
}
