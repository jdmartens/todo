import { Routes } from '@angular/router';
import { TaskListComponent } from './task-list/task-list.component';
import { TaskFormComponent } from './task-form/task-form.component';

export const routes: Routes = [
    { path: '', redirectTo: '/todos', pathMatch: 'full' },
    { path: 'todos', component: TaskListComponent },
    { path: 'todo/new', component: TaskFormComponent },
    { path: 'todo/:id', component: TaskFormComponent }
];

  
