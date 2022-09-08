import { createStore } from 'vuex'
import axios from "axios"
import { getMyToken } from '../service';

export default createStore({
  state: {
    host: 'https://antonioglyzin.pythonanywhere.com/api',
    // host: 'http://127.0.0.1:8000/api',
    // host: 'https://antonio-api.herokuapp.com/api',:${window.location.port}/
    // host: `${window.location.protocol}//${window.location.hostname}:${window.location.port}/api`,
    // host: `${window.location.protocol}//${window.location.hostname}/api`,
    poems: [],
    pagePoems:[],
    countPoems:0,
    isLoaded:0,
    curPage:0
  },
  mutations:{
    SET_POEMS_TO_STATE: (state, poems) => {
        state.poems = poems;
    },
    SET_PAGE_POEM: (state, res) => {
      state.pagePoems = res;
    },
    SET_COUNT_POEM: (state, res) => {
      state.countPoems = res;
    },
    SET_LOADED(state, res){
      state.isLoaded = res;
    },
    SET_CUR_PAGE(state, res){
      state.curPage = res;
    }
  },
  actions:{
    GET_POEMS_FROM_API({commit}, url) {
      commit('SET_LOADED',0)
      commit('SET_PAGE_POEM', []);
        return axios(this.state.host+url, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          }
        })
          .then((res) => {
            if(res.data.length){
              commit('SET_COUNT_POEM', res.data.length);
              let poemPage = 8
              let poems = res.data
              let pages = []
              let countPage = Math.ceil(poems.length / poemPage)
              for(let i = 1; i <= countPage; i++){
                  let onePage = []
                  for(let j = 1; j <= poemPage; j++){
                      let poem = poems.shift()
                      if(poem==undefined) continue
                      onePage.push(poem)
                  }
                  pages.push(onePage)
              }
              commit('SET_PAGE_POEM', pages);
              commit('SET_LOADED',1)
            }else if(res.data.length==0){
              commit('SET_PAGE_POEM', []);
              commit('SET_COUNT_POEM', res.data.length);
              
            }
            else{
              var arr = []
              var resPoem = res.data
              axios.get(this.state.host+`/poems/comment/me/${res.data.id}/`,{
                headers:{
                  'X-CSRFToken':getMyToken()
                }
              })
              .then(res=>{
                arr = res.data.map(item => {return item.id})
                resPoem.me_comment = arr
                commit('SET_POEMS_TO_STATE', resPoem);
                commit('SET_LOADED',1)
              })
              
            }
          })
          .catch((error) => {
            return error;
          })
      },
    SAVE_CUR_PAGE({commit},num){
      commit('SET_CUR_PAGE', num)
    }
  },
  getters:{
    GET_POEMS(state){
        return state.poems
    },
    GET_HOST(state){
      return state.host
    },
    GET_PAGES_POEM(state){
      return state.pagePoems
    },
    GET_COUNT_POEM(state){
      return state.countPoems
    },
    IS_LOADED(state){
      return state.isLoaded
    },
    GET_CUR_PAGE(state){
      return state.curPage
    }
  },
})

