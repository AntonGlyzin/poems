import {createApp} from 'vue'
import App from './App.vue'
import store from './components/vuex/store'
import './assets/styles/styles.scss'
import router from "./components/router/router"
import './assets/styles/font-awesome.min.css'

createApp(App)
    .use(router)
    .use(store)
    .mount('#app')
