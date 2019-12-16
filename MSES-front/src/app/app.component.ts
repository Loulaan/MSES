import { Component } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import * as Chokidar from 'chokidar';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'MSES';


  video: any;
  direction: any = {
    direction: 'left'
  };
  isRedUp = true;
  isYellowUp = false;
  isGreenUp = false;
  isRedDown = true;
  isYellowDown = false;
  isGreenDown = false;
  fileName = '';
  loading = false;
  constructor(
    private http: HttpClient
  ) { }

  fileChange(event): void {
    console.log(this.video);
    this.deleteVideo();
    console.log(this.video);
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file = fileList[0];
      this.fileName = file.name;
      const formData = new FormData();
      formData.append('file', file, file.name);
      this.loading = true;
      this.http.post('http://localhost:8080/', formData,
        { headers: new HttpHeaders({ enctype: 'multipart/form-data', Accept: 'application/json' }), responseType: 'blob' })
        .subscribe((resp: Blob) => {
            this.createImageFromBlob(resp);
            console.log(this.video);
            this.http.get('http://localhost:8080/direction').subscribe((resp1) => {
              this.direction = resp1;
              this.trafficLight();
            });
        }, () => this.loading = false,
          () => this.loading = false
        );
    }
  }

  trafficLight(): void {
    if ( this.direction.direction === 'left') {
      console.log('here');
      setTimeout(() => {
        this.isRedUp = false;
        this.isYellowUp = true;
      }, 1000);
      setTimeout(() => {
        this.isYellowUp = false;
        this.isGreenUp = true;
      }, 2000);
      setTimeout(() => {
        this.isGreenUp = false;
        this.isRedUp = true;
      }, 3000);
    }
    if ( this.direction.direction === 'right') {
      setTimeout(() => {
        this.isRedDown = false;
        this.isYellowDown = true;
      }, 1000);
      setTimeout(() => {
        this.isYellowDown = false;
        this.isGreenDown = true;
      }, 2000);
      setTimeout(() => {
        this.isGreenDown = false;
        this.isRedDown = true;
      }, 3000);
    }
  }

  createImageFromBlob(video: Blob) {
    const reader = new FileReader();
    reader.addEventListener('load', () => {
      this.video = reader.result;
    }, false);

    if (video) {
      reader.readAsDataURL(video);
    }
  }

  videoClick(): void {
    this.trafficLight();
  }

  deleteVideo(): void {
    this.video = undefined;
  }
}
