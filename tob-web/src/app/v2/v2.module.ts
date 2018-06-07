import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LocalizeRouterModule } from 'localize-router';
import { Routes, RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { CredModule } from '../cred/cred.module';
import { SearchModule } from '../search/search.module';

import { HomeComponent } from '../home/home.component';
import { SubjectFormComponent } from '../subject/form.component';

export const ROUTES: Routes = [
  {
    path: 'v2',
    redirectTo: 'v2/home',
    pathMatch: 'full'
  },
  {
    path: 'v2/home',
    component: HomeComponent,
    data: {
      breadcrumb: 'dashboard.breadcrumb'
    }
  },
  {
    path: 'v2/subject/:subjId',
    component: SubjectFormComponent,
    data: {
      breadcrumb: 'org.breadcrumb'
    }
  }
];

@NgModule({
  declarations: [
    HomeComponent,
    SubjectFormComponent,
  ],
  imports: [
    CommonModule,
    CredModule,
    SearchModule,
    RouterModule.forChild(ROUTES),
    TranslateModule.forChild(),
    LocalizeRouterModule.forChild(ROUTES),
  ],
})
export class v2Module {}