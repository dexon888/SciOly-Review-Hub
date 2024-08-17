import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from'../environments/environment'

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  generateQuiz(topic: string, mcqCount: number, srqCount: number): Observable<any> {
  return this.http.post<any>(`${this.apiUrl}/generate-quiz`, { topic, mcqCount, srqCount });
}

}
