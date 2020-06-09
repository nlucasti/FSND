import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

import { ActorsPage } from './actors.page';

describe('ActorsPage', () => {
  let component: ActorsPage;
  let fixture: ComponentFixture<ActorsPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ActorsPage],
      imports: [IonicModule.forRoot(), ExploreContainerComponentModule]
    }).compileComponents();

    fixture = TestBed.createComponent(ActorsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
