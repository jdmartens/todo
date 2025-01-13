import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { TaskService } from '../task.service';
import { CommonModule } from '@angular/common';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

@Component({
  selector: 'app-task-form',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatInputModule,
    MatButtonModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  templateUrl: './task-form.component.html',
  styleUrl: './task-form.component.scss'
})
export class TaskFormComponent implements OnInit {
  taskForm: FormGroup;
  isEditMode: boolean = false;
  taskId: string = 'new';

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private taskService: TaskService
  ) {
    this.taskForm = this.fb.group({
      task_name: ['', Validators.required],
      due_date: ['', Validators.required],
      due_time: ['', Validators.required],
      status: ['pending', Validators.required],
      type: ['personal', Validators.required]
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params['id'] && params['id'] !== 'new') {
        this.isEditMode = true;
        this.taskId = params['id'];
        this.loadTask(this.taskId);
      }
    });
  }

  loadTask(id: string): void {
    this.taskService.getTask(id).subscribe(
      (task) => {
        const dueDate = new Date(task.due_date);
        this.taskForm.patchValue({
          ...task,
          dueDate: dueDate,
          due_time: this.formatTime(dueDate)
        });
      },
      (error) => {
        console.error('Error loading task:', error);
      }
    );
  }

  onSubmit(): void {
    if (this.taskForm.valid) {
      const formData = this.taskForm.value;
      const dueDate = new Date(formData.due_date);
      const [hours, minutes] = formData.due_time.split(':').map(Number);
      dueDate.setHours(hours, minutes);

      const taskData = {
        ...formData,
        id: this.taskId,
        due_date: dueDate,
      };
      console.log('Due date:', dueDate, hours, minutes, taskData);

      if (this.isEditMode) {
        this.taskService.updateTask(this.taskId, taskData).subscribe({
          next: () => {
            this.router.navigate(['/todos']);
          },
          error: (error) => {
            console.error('Error updating task:', error);
          }
        });
      } else {
        this.taskService.addTask(taskData).subscribe({
          next: () => {
            this.router.navigate(['/todos']);
          },
          error: (error) => {
            console.error('Error adding task:', error);
          }
        });
      }
    }
  }

  private formatTime(date: Date): string {
    return date.toTimeString().substring(0, 5);
  }
}
