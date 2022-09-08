<template>
    <nav>
        <ul id="navlist">
        <li><i style="margin-right: 5px" class="fa fa-music" aria-hidden="true"></i>Стихи
                            <ul>
                                <li v-for="item in menu" :key="item.slug" @click="click_menu(`/poems/cat/${item.slug}`)">{{item.name}}</li>
                                <li @click="click_menu('/poems/')">✪ разные</li>

                            </ul></li>
        
            <li @click="click_menu('/poems/win')">
                <i style="margin-right: 5px" class="fa fa-trophy" aria-hidden="true" ></i>
                Награды
            </li>
        </ul>
    </nav>
</template>

<script>
import axios from "axios"
import {mapGetters} from 'vuex'
export default {
    name: 'site-menu',
    data(){
        return{
            menu:[]
        }
    },
    components:{},
    methods: {
        click_menu(link='/'){
            this.$router.push(link)
        }
    },
    computed:{
        ...mapGetters([
            'GET_HOST',
        ]),
    },
    mounted() {
        axios.get(this.GET_HOST+'/poems/all/category/').then(res=>{
            this.menu = res.data
        })
    },
}
</script>

<style lang='scss'>

#navlist{
    padding: 8px 0 8px;
	margin-left: 130px;
	list-style-type: none;
	color: #666666;
    display: flex;
    width: 338px;

    &>li{
        padding: 6px 16px;
        position: relative;
        box-sizing: border-box;
        &:hover{
            cursor: pointer;
            color: #333333;
            border-bottom: 1px solid #333333;

            &>ul{
                visibility: visible;
                height: auto;
                color: #666666;
                top: 32px;
                li:hover{
                    color: #333333;
                }
            }
        }

        ul{
            list-style-type: none;
            position: absolute;
            padding: 7px 0;
            background-color: rgba(232, 232, 232, 0.9);
            box-sizing: border-box;
            top: 60px;
            left: -6px;
            overflow: hidden;
            visibility: hidden;
            height: 0;
            transition: top 300ms;
            li{
                min-width:185px;
                box-sizing: border-box;
                padding: 6px 16px;
                &:after{
                    content: '';
                    display: block;
                    height: 1px;
                    margin-top: 7px;
                    width: 100%;
                    background-color:  #c9c9c9;
                    
                }
                &:hover::after{
                    content: '';
                    display: block;
                    height: 1px;
                    margin-top: 7px;
                    width: 100%;
                    background-color: #7a7a7a;
                }
            }
        }
    }
}

</style>