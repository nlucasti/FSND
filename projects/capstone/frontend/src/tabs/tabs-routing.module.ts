import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      {
        path: 'movies',
        loadChildren: () => import('../movies/movies.module').then(m => m.MoviesPageModule)
      },
      {
        path: 'actors',
        loadChildren: () => import('../actors/actors.module').then(m => m.ActorsPageModule)
      },
      {
        path: 'tab3',
        loadChildren: () => import('../tab3/tab3.module').then(m => m.Tab3PageModule)
      },
      {
        path: '',
        redirectTo: '/tabs/movies',
        pathMatch: 'prefix'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/movies',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}
