import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule, TitleCasePipe } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-question-generator',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './question-generator.component.html',
  styleUrls: ['./question-generator.component.css'],
  providers: [TitleCasePipe]
})
export class QuestionGeneratorComponent implements OnInit {
  topic: string | null = null;
  mcqCount: number = 0;
  srqCount: number = 0;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService,
    private titleCasePipe: TitleCasePipe
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.topic = params.get('topic');
      if (this.topic) {
        this.topic = this.titleCasePipe.transform(this.topic);
      }
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
