import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { AppCardComponent } from './components/app-card/app-card.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { AppStoreComponent } from './pages/app-store/app-store.component';
import { DepartmentAppsComponent } from './pages/department-apps/department-apps.component';

const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'app-store', component: AppStoreComponent },
  { path: 'department-apps', component: DepartmentAppsComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    AppCardComponent,
    DashboardComponent,
    AppStoreComponent,
    DepartmentAppsComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }