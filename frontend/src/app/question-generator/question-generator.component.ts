import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { ApiService } from '../api.service';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { QuestionDisplayComponent } from '../question-display/question-display.component';

@Component({
  selector: 'app-question-generator',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule, FormsModule, QuestionDisplayComponent],
  templateUrl: './question-generator.component.html',
  styleUrls: ['./question-generator.component.css']
})
export class QuestionGeneratorComponent implements OnInit {
  topic: string | null = null;
  question: string | null = null;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.topic = params.get('topic');
      this.question = null; // Reset the question when topic changes
    });
  }

  generateQuestion(): void {
    if (this.topic) {
      this.apiService.generateQuestion(this.topic).subscribe(
        (response: any) => {
          this.question = response.question;
        },
        (error: any) => {
          console.error('Error generating question:', error);
        }
      );
    }
  }
}
