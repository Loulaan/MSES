import { Component, OnInit } from '@angular/core';
@Component({
  selector: 'app-traffic-light',
  templateUrl: './traffic-light.component.html',
  styleUrls: ['./traffic-light.component.css']
})
export class TrafficLightComponent implements OnInit {
  isRed = true;
  isYellow = false;
  isGreen = false;
  constructor() { }

  ngOnInit() {
  }

}
