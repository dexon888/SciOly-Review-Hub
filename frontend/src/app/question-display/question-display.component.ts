import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-question-display',
  standalone: true,  // Ensure this is a standalone component
  templateUrl: './question-display.component.html',
  styleUrls: ['./question-display.component.css'],
  imports: [CommonModule]  // Import CommonModule here
})
export class QuestionDisplayComponent implements OnInit {
  quiz: string[] | null = null;

  constructor(private router: Router) {}

  ngOnInit(): void {
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras?.state) {
      this.quiz = navigation.extras.state['quiz'] || null;
    }

    console.log('Quiz data:', this.quiz);
  }
}
