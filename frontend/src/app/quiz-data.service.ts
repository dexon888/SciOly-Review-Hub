import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class QuizDataService {
  private quizData: any = null;

  setQuizData(data: any): void {
    this.quizData = data;
  }

  getQuizData(): any {
    return this.quizData;
  }
}
