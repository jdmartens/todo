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

  openAddTaskForm(): void {
    // this.taskService.deleteTask(id).subscribe(
    //   () => {
    //     this.loadTasks();
    //   },
    //   (error) => {
    //     console.error('Error deleting task:', error);
    //   }
    // );
  }

  editTask(id: string): void {
    this.router.navigate(['/todo', id]);
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
