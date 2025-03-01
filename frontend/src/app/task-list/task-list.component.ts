import { Component, OnInit } from '@angular/core';
import { TaskService } from '../task.service';
import { MatTableModule } from '@angular/material/table';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [
    MatTableModule,
    DatePipe,
  ],
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.scss']
})
export class TaskListComponent implements OnInit {
  tasks: any[] = [];
  displayedColumns: string[] = ['task_name', 'due_date', 'status', 'actions'];

  constructor(
    private taskService: TaskService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadTasks();
  }

  loadTasks(): void {
    this.taskService.getTasks().subscribe(
      (data) => {
        this.tasks = data;
      },
      (error) => {
        console.error('Error fetching tasks:', error);
      }
    );
  }

  addTask(): void {
    this.router.navigate(['/todo', 'new']);
  }

  editTask(id: string): void {
    this.router.navigate(['/todo', id]);
  }

  completeTask(id: string): void {
    const taskData = {
      id: id,
      status: 'completed'
    };
    this.taskService.completeTask(id, taskData).subscribe({
      next: () => {
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error updating task:', error);
      }
    });
  }

  deleteTask(id: string): void {
    this.taskService.deleteTask(id).subscribe(
      () => {
        this.loadTasks();
      },
      (error) => {
        console.error('Error deleting task:', error);
      }
    );
  }
}
