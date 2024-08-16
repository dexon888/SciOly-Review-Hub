import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';  // Import FormsModule for two-way binding

interface QuizItem {
  type: string;
  question: string;
  options?: string[];  // Array of options for multiple-choice questions
  selectedOption?: string;  // To store the selected answer
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

  constructor(private router: Router) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras?.state) {
      this.quiz = navigation.extras.state['quiz'] || null;
      this.topic = navigation.extras?.state?.['topic'] || 'Quiz';  // Assuming 'topic' is passed
      this.topic = this.topic ? this.capitalizeFirstLetter(this.topic) : null;
    }
  }

  capitalizeFirstLetter(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  ngOnInit(): void {}

  submitQuiz(): void {
    console.log('Submitted Quiz:', this.quiz);
    // Add logic to handle quiz submission, like sending data to the backend
  }
}
