<template>
    <div class='main-content'>
            <div id='countstih-id' class="countstih">Стихотворений на странице - {{this.GET_COUNT_POEM}} шт.</div>
            <div class="main-content-book"></div>
            <div class="sort-block">
                <p>Сортировка по - </p>
                <div class="box">
                <select v-model="sortSearch" @change="sortPost()">
                    <option value='ordering=-count_comments'>комментариям - убывание</option>
                    <option value='ordering=count_comments'>комментариям - возрастание</option>
                    <option value='ordering=-count_view'>просмотрам - убывание</option>
                    <option value='ordering=count_view'>просмотрам - возрастание</option>
                    <option value='ordering=-time_create'>дате - убывание</option>
                </select>
                </div>
            </div>
            

            <i v-if="isLoad==0" class="load-spin fa fa-spinner fa-pulse fa-3x fa-fw"></i>
            <div class="main-content-poems">
                <div  class="main-content-poems-item" @click="got_to_poem(poem.slug)" v-for="poem in listPoems[currentPage]" :key="poem.id">
                    <h1>{{poem.title}}</h1>
                    <div class="main-content-poems-item-info">
                        <i class="fa fa-user" aria-hidden="true"></i><p>{{poem.get_author}}</p>
                        <i class="fa fa-calendar" aria-hidden="true"></i><p>{{poem.time_create}}</p>
                        <i class="fa fa-comment" aria-hidden="true"></i><p>{{poem.count_comments}}</p>
                        <i class="fa fa-eye" aria-hidden="true"></i><p>{{poem.count_view}}</p>
                    </div>
                    <div class="main-content-poems-item-img">
                        <div class="main-content-poems-item-img-inner"></div>
                        <div class="main-content-poems-item-art" :style="{ backgroundImage: `url(${poem.photo})`  }" />
                    </div>
                    <i class="heart fa fa-eye" aria-hidden="true"></i>
                </div>
            </div>

                <ul class="pagination">
                    <li @click="currentPage ? --currentPage:currentPage">«</li>
                    <li v-for="num in listNum" :key="num" @click="setPage(num)" :class="currentPage==num ?'active' : ''">{{num+1}}</li>
                    <li @click="1+currentPage<listNum.length ? ++currentPage:currentPage">»</li>
                    </ul>
        </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
export default {
    name: 'poems-page',
    props: {
        catId: {
            type: String,
            default: null,
        },
        searchVal: {
            type: String,
            default: null,
        },
        
    },
    data() {
        return {
            currentPage:0,
            numPages:1,
            sortSearch:'',
        }
    },
    methods: {
        ...mapActions([
        'GET_POEMS_FROM_API',
        'SAVE_CUR_PAGE'
        ]),
        setPage(num=0){
            this.currentPage = num
        },
        got_to_poem(link='reht'){
            this.$router.push(`/poems/poem/${link}`)
        },
        getPage(){
            let path = this.$router.currentRoute._rawValue.fullPath
            this.GET_POEMS_FROM_API(path)
            
        },
        sortPost(){
            this.setPage()
            this.$router.push(`?${this.sortSearch}`)
            let path = this.$router.currentRoute._rawValue.path
            this.GET_POEMS_FROM_API(path+`?${this.sortSearch}`)
        }
    },
    computed:{
        ...mapGetters([
            'GET_POEMS',
            'GET_PAGES_POEM',
            'GET_COUNT_POEM',
            'IS_LOADED',
            'GET_CUR_PAGE'
        ]),
        isLoad(){
            return this.IS_LOADED
        },
        listPoems(){
            return this.GET_PAGES_POEM
        },
        listNum(){
            let len = []
            let dd = this.listPoems.length
            
            for(let i=0; i<dd; i++) len.push(i)
            return len
        }

    },
    watch:{
        catId(){
            this.getPage()
            this.setPage()
            this.sortSearch = ''
        },
        searchVal(){
            this.getPage()
            
        },
        currentPage(){
            document.getElementById('countstih-id').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
                })
        },
    },
    mounted() {
        this.getPage()
        this.setPage(this.GET_CUR_PAGE)
    },
    updated() {
        document.querySelector("title").innerHTML = 'Стихи - «Любовь за гранью звёзд»'
    },
    unmounted() {
        this.SAVE_CUR_PAGE(this.currentPage)
    },
}
</script>

<style lang="scss">
.load-spin{
    margin-left: 139px;
    margin-top: 21px;
}
main{
        .sort-block{
            position: relative;
            display: flex;
            p{
                    padding-top: 7px;
                    padding-right: 11px;
            }
        }
        .box {
            position: relative;
            
            // transform: translate(-50%, -50%);
            
        }

        .box select {
            background-color: #e6e1d9;
            color: #222222;
            padding: 6px;
            width: 222px;
            border: 1px solid #4545;
            font-size: 1em;
            -webkit-appearance: button;
            appearance: button;
            outline: none;

            &:hover, &:active, &:focus{
                cursor: pointer;
                border: 1px solid #00000080;
            }
        }

        .box:hover::before {
            color: rgba(255, 255, 255, 0.6);
            background-color: rgba(255, 255, 255, 0.2);
        }

        .box select option {
            padding: 30px;
        }

        .main-content{
            width: 422px;
            margin-left: 88px;
            padding-left: 26px;
            box-sizing: border-box;

                ul.pagination {
                display: flex;
                padding: 0;
                margin-top: 32px;
                justify-content: center;
                }

            ul.pagination li {display: inline;}

            ul.pagination li {
                color: black;
                float: left;
                padding: 8px 16px;
                text-decoration: none;
                &:hover{
                    cursor: pointer;
                }
            }

            ul.pagination .active {
                background-color: #686c4a;
                color: white;
            }

            ul.pagination li:hover:not(.active) {background-color: #ddd;}
        }
        .countstih{
            padding-top: 30px;
        }
        .main-content-poems{
            width: 356px;
            
            &-item{
                padding-top: 50px;
                position: relative;

                & .heart{
                    position: absolute;
                    font-size: 153px;
                    transform: translate(99px, -178px);
                    opacity: 0;
                    transition: opacity 500ms;
                }

                &:first-child{
                    padding-top: 19px;
                }
                &-info{
                    display: flex;
                    color: #686c4a;
                    font-size: .8em;
                    padding-left: 27px;
                    transition: color 400ms;
                    padding-bottom: 8px;
                    p{
                        padding-left: 5px;
                        padding-right: 15px;
                    }
                }
                 &:hover .heart{
                    opacity: .5;
                 }
                &:hover {
                    cursor: pointer;
                }
                &:hover h1{
                    color: #474936;
                }
                &:hover .main-content-poems-item-info{
                    color: #474936;
                }
                &:hover .main-content-poems-item-img{
                    box-shadow: 0px 5px 4px #818181;
                }
                h1{
                    color: #686c4a;
                    font-size: 1.3em;
                    padding-bottom: 9px;
                    transition: color 400ms;
                }
                &-img{
                        height: 212px;
                        width: 354px;
                        box-sizing: border-box;
                        position: relative;
                        display: flex;
                        justify-content: center;
                         background-color: #f0f0f0;

                        border: 2px solid #91919144;
                    padding: 6px;
                    border-block-color: #4494;
                    box-shadow: 0px 2px 2px #818181;
                    transition: box-shadow 400ms;

                    &-inner{
                        width: 90%;
                        height: 90%;
                        position: absolute;
                        background-color: #222222;
                    }

                        &:before,
                    &:after {
                        background: rgba(255,255,235,.6);
                        box-shadow: 0 1px 3px rgba(0,0,0,.4);
                        content: "";
                        display: block;
                        height: 24px;
                        position: absolute;
                        margin: auto;
                        width: 82px;
                        opacity: 0.6;
                        z-index: 1;
                    }
                    &:after{
                        right: -9px;
                        top: -9px;
                    }
                    &:before{
                        left: -9px;
                        top: -9px;
                    }

                }
                &-art{
                    box-sizing: border-box;
                    background-size: contain;
                    z-index: 0;
                    position: absolute;
                    width: 88%;
                    height: 88%;
                    background-position: center;
                    background-repeat: no-repeat;
                    margin-top: 2px;

                }
            }
        }
    }
</style>