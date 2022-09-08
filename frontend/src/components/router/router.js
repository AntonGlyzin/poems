
import { createRouter, createWebHistory } from "vue-router"

import pagePoems from '../../components/page-site/poems-page'
import pagePoemSingle from '../../components/page-site/single-poem'
import pageWin from '../../components/page-site/win-page'



const routeInfos = [
    {
        path: '/poems/',
        name: 'page-poems',
        component: pagePoems,
        props: true,
        children:[
            {
                path: '/poems/cat/:catId/',
                name: 'cat-poems',
                component: pagePoems
            },
            {
                path: '/poems/search/:searchVal',
                name: 'search-poems',
                component: pagePoems
            }
        ]
    },
    {
      path: '/poems/poem/:nameId',
      name: 'poem-single',
      component: pagePoemSingle,
      props: true
    },
    {
        path: '/poems/win/',
        name: 'page-win',
        component: pageWin
    },
  ]

const router = createRouter({
    history : createWebHistory(),
    routes : routeInfos
})

export default router;