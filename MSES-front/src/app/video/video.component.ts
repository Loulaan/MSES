import {Component, Input, OnInit} from '@angular/core';
import * as Chokidar from 'chokidar';

@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.css']
})
export class VideoComponent implements OnInit {
  VIDEO_PATH = '../../../../WEB_DATA/out/4.mp4';
  @Input() play: boolean;
  constructor() { }

  ngOnInit() {
  }

}
