import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { QuestionGeneratorComponent } from './question-generator/question-generator.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'quiz/:topic', component: QuestionGeneratorComponent }
];
