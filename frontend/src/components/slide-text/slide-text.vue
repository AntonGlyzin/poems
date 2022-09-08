<template>
   <div class="slide-text">
       <h3 class="slide-text-head-stih" >Все рецензии к произведениям на сайте - <a target="_blank" href="https://stihi.ru/rec_author.html?toshaglyzin">Стихи.ру</a></h3>
       <div class="count-comment">Всего комментариев на сайте - {{countComment}} </div>
        <!-- <div class="slide--parent  js-flickity" data-flickity-options='{ "cellAlign": "left", "contain": true }'> -->
            <div class="slide--parent" >
            <div class="parent--el" v-for="comment in comments" :key="comment.id">
                <div class="two--col">
                    <div class="is-item has--content">
                        <div class="is-item--inner" >
                <h3> {{comment.name}} | <div class='parent--el-link' @click="goToPoem(comment.poem.slug)" >{{comment.poem.title}}</div></h3>

                        <p>{{comment.body}}</p>

                        </div>
                    </div>
                </div>
            </div>
        
        
  	    </div>
   </div>
</template>

<script>
import '../../assets/js/flickity.pkgd.min.js'
import axios from "axios"
import {mapGetters} from 'vuex'
export default {
    name: 'slide-text',
    data() {
        return {
            comments:[],
            countComment:0
        }
    },
    components:{
    },
    methods: {
        goToPoem(slug){
            this.$router.push(`/poems/poem/${slug}`)
        },
    },
    computed:{
        ...mapGetters([
            'GET_HOST',
        ]),
    },
    mounted() {
        axios.get(this.GET_HOST+'/poems/comment/').then(res=>{
            this.countComment = res.data
        })
        axios.get(this.GET_HOST+'/poems/comment/21/')
            .then(res => {
                this.comments = res.data

                setTimeout(()=>{
                    var flk = new Flickity( '.slide--parent', {
                    // Настройки плагина
                    cellAlign: 'left',
                    contain: true 
                    });
                }, 1000)
            })
        
    },
}
</script>

<style lang="scss">
@import url('../../assets/styles/flickity.min.css');
.count-comment{
        margin-left: 51px;
    font-size: 1.3em;
    margin-bottom: 16px;
    font-style: italic;
}
.flickity-prev-next-button .arrow {
    fill: #b3b1b1;
}
.slide-text-head-stih{
    margin-left: 28px;
    font-size: 1.35em;
    font-style: italic;
    padding-bottom: 25px;
    a, a:active {
        color: #666666;
        text-decoration: none;
    }
    a:hover {
    color: #333333;
    }
}
.slide-text{
    margin-left: -160px;
    padding-bottom: 71px;
    padding-left: 22px;
}
.slide--parent { 
overflow: hidden;   
width:577px;
color: #1a1a1a;
}
.is-item { width: 577px; }

.parent--el .two--col { display: flex; align-items: center; }
figure { margin: 0; }

.is-item--inner { 
    padding: 0em 4em; 
        font-style: italic;
    h3{
        padding-bottom: 15px;
        box-sizing: border-box;
        font-size: 1.35em;
        display: flex;
        div{
                margin-left: 6px;
                cursor: pointer;
                color: #666666;
                &:hover{
                        color: #333333;
                }
        }
    }

    a, a:active {
        color: #666666;
        text-decoration: none;
    }
    a:hover {
    color: #333333;
    }
    p{
        font-size: 1.35em;
            padding-left: 5px;
    }
}
</style>