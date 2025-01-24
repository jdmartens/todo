import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getTasks(): Observable<any> {
    return this.http.get(`${this.apiUrl}/tasks`);
  }

  getTask(id: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/task/${id}`);
  }

  addTask(task: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/tasks/`, task);
  }

  updateTask(id: string, task: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/tasks/${id}`, task);
  }

  completeTask(id: string, task: { status: string }): Observable<any> {
    return this.http.put(`${this.apiUrl}/tasks/${id}/complete`, task);
  }

  deleteTask(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/tasks/${id}`);
  }
}
