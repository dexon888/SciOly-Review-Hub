import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

interface QuizItem {
  type: string;
  question: string;
}

@Component({
  selector: 'app-question-display',
  standalone: true,
  templateUrl: './question-display.component.html',
  styleUrls: ['./question-display.component.css'],
  imports: [CommonModule]
})
export class QuestionDisplayComponent {
  quiz: QuizItem[] | null = null;

  constructor(private router: Router) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras?.state) {
      this.quiz = navigation.extras.state['quiz'] || null;
    }
  }
}
