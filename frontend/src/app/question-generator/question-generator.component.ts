import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-question-generator',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './question-generator.component.html',
  styleUrls: ['./question-generator.component.css']
})
export class QuestionGeneratorComponent implements OnInit {
  topic: string | null = null;
  mcqCount: number = 0;
  srqCount: number = 0;

  constructor(private route: ActivatedRoute, private router: Router, private apiService: ApiService) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.topic = params.get('topic');
    });
  }

  generateQuiz(): void {
    if (this.topic) {
      this.apiService.generateQuiz(this.topic, this.mcqCount, this.srqCount).subscribe(
        (response: any) => {
          this.router.navigate(['/quiz-display'], { state: { quiz: response.quiz } });
        },
        (error: any) => {
          console.error('Error generating quiz:', error);
        }
      );
    }
  }
}
