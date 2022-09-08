<template>
    <div id='main-content-single-id' class='main-content-single'>
        
            <div class="main-content-single-item" >
                    <h1>{{listPoems.title}}</h1>
                    <div class="main-content-single-item-info">
                        <i class="fa fa-user" aria-hidden="true"></i><p>{{listPoems.get_author}}</p>
                        <i class="fa fa-calendar" aria-hidden="true"></i><p>{{listPoems.time_create}}</p>
                        <i class="fa fa-comment" aria-hidden="true"></i><p>{{listPoems.count_comments}}</p>
                        <i class="fa fa-eye" aria-hidden="true"></i><p>{{listPoems.count_view}}</p>
                    </div>
                    <div class="main-content-single-item-img">
                        <div class="main-content-single-item-img-inner"></div>
                        <div class="main-content-single-item-art" :style="{ backgroundImage: `url(${listPoems.photo})`  }" />
                    </div>
                    <i v-if="isLoad==0" class="load-spin fa fa-spinner fa-pulse fa-3x fa-fw"></i>
                    <p v-html="listPoems.content"></p>

                    <a :href="listPoems.link_stih" class="link-stih" target="_blank">
                        <img src="../../assets/images/stihiru.png" height=30 alt="" style="margin-top: 20px;">
                    </a>

                <div class="main-content-single-comment">


                    <div class="commentAuthor" id_comm="0" v-for="comment in listPoems.comments" :key="comment.id">
                            <div class="commentAuthorName"><i class="fa fa-user-circle" aria-hidden="true"></i><p>{{comment.name}}</p></div>
                            <div class="commentAuthorText"><p>{{comment.body}}</p>
                            <div class="btn-wrp">
                                <button @click="delComment(comment.id)" class="commentDel" v-if="listPoems.me_comment.includes(comment.id)" ><i class="fa fa-trash" aria-hidden="true"></i> Удалить</button>
                            </div>
                            
                            </div>
                            

                    </div>
                            


                        <div v-if="flagMsg" :style="msgColor" class='result' ><i :class="msgIcon" aria-hidden="true"></i>
                            {{resultSend}}
                        </div>

                    <form name="commentform" class="commentform">
                                <textarea v-model="bodyComment" name="body" cols="45" rows="8" class="formcommtext" placeholder="Сообщение" required="" id="id_body"></textarea>
                                <div v-if="isCaptch" class="captch-wrp">
                                     <img :src="getHostCaptcha+imgCaptch" alt="captcha" class="captcha">
                                    <input type="hidden" name="captcha_0" :value="keyCaptch" required="" id="id_captcha_0">
                                    <input type="text" name="captcha_1" required="" id="id_captcha_1" autocapitalize="off" autocomplete="off" 
                                    autocorrect="off" spellcheck="false" v-model="captchInput">
                                </div>
                                
                            
                                <input type="text" v-model="nameComent" name="name" class="formcommauthor" placeholder="Имя" required="" size="15" maxlength="80" id="id_name">
                              <!-- <div class="commentform-wrp">  <input type="email" v-model="emailComment" name="email" class="formcommemail" placeholder="Email (по желанию)" size="15" maxlength="254" id="id_email">
                            </div> -->
                                
                            
                        <div  class="input-submit-mess" @click="sendComment()" >Отправить<i class="fa fa-paper-plane" aria-hidden="true"></i></div>
                    </form>
                        </div>
                </div>
    </div>
</template>

<script>
import { getMyToken } from '../service';
import axios from "axios"
import {mapActions, mapGetters} from 'vuex'
import $ from 'jquery';
import Cookies from 'js-cookie'
export default {
    name: 'single-poems',
    props: {
        nameId: {
            type: String,
            default: null,
        },
    },
    data() {
        return {
            nameComent:'',
            bodyComment:'',
            emailComment:'',
            keyCaptch:'',
            imgCaptch:'',
            captchInput:'',
            resultSend: '',
            isCaptch:false,
            msgIcon:'',
            msgColor:'',
            flagMsg: 0,

            customKeyWords:''           
        }
    },
    methods: {
        ...mapActions([
        'GET_POEMS_FROM_API',
        ]),
        delComment(id){
            axios.get(this.GET_HOST+`/poems/comment/${id}/`,{
                headers:{
                    'X-CSRFToken':getMyToken()
                }
            }).then(res=>{
                this.refreshPage()
            })
        },
        windowArt(){
            $('.main-content-single-item-art').click(function(){
                let src = $(this).attr('style')
                $("body").append(`<div class='popup-art_bk'><div class='popup-art' style='${src}'></div></div>`);
                $(".popup-art").fadeIn(200);
                $(".popup-art_bk").click(function(){	
                    $(".popup-art").fadeOut(200);	
                    setTimeout(function() {	
                            $(".popup-art_bk").remove(); 
                            }, 200);
                });
            })
        },
        sendComment(){
            if(!this.keyCaptch){
                this.getCaptcha()
                this.isCaptch = true
                return
            }
            var csrftoken = getMyToken()
            let data = {
                poem: this.listPoems.id,
                name: this.nameComent,
                email: this.emailComment,
                body: this.bodyComment,
                captcha_0: this.keyCaptch,
                captcha_1: this.captchInput
            }

            axios({
                method:'post',
                url:this.GET_HOST+'/poems/add/comment/',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken':csrftoken
                },
                data: JSON.stringify(data)
            })
            .then(res => {
                if(res.data=='captcha=old'){
                    this.flagMsg = 1
                    this.resultSend = 'Капча устарела или была добушенна ошибка.'
                    this.msgIcon = 'fa fa-exclamation'
                    this.msgColor = 'background-color: #bf8575;'
                    this.captchInput = ''
                    this.getCaptcha()
                    setTimeout(()=>{
                        this.flagMsg=0
                    },5000)
                }
                else if(res.data=='sended'){
                    this.flagMsg = 1
                    this.resultSend = 'Ваш комментарий отправлен!'
                    this.msgIcon = 'fa fa-check-circle'
                    this.msgColor = 'background-color: #97cf99;'
                    this.nameComent = ''
                    this.emailComment = ''
                    this.bodyComment = ''
                    this.captchInput = ''

                    let path = this.$router.currentRoute._rawValue.fullPath
                    this.GET_POEMS_FROM_API(path)
                    setTimeout(()=>{
                        this.flagMsg=0
                    },5000)
                }
            }).catch(res=>{
                this.flagMsg = 1
                this.resultSend = 'Ошибка отправления.'
                this.msgIcon = 'fa fa-times-circle'
                this.msgColor = 'background-color: #bf8575;'
                setTimeout(()=>{
                        this.flagMsg=0
                    },5000)
            })
        },
        getCaptcha(){
            // axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
            
            axios.get(this.GET_HOST+'/captcha/refresh/',{
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                }
            })
            .then(res => {
                this.keyCaptch = res.data.key
                this.imgCaptch = res.data.image_url

                if(!Cookies.get('csrftoken')){
                    axios.get(this.GET_HOST+'/getprotect/').then(res=>{
                            Cookies.set('csrftoken', res.data['token'], { expires: 365 })
                    })
                }
            })
        },
        refreshPage(){
            let path = this.$router.currentRoute._rawValue.fullPath
            this.GET_POEMS_FROM_API(path)
            this.flagMsg = 0
            this.nameComent = ''
            this.emailComment = ''
            this.bodyComment = ''
            this.captchInput = ''
        }
    },    
    computed:{
        ...mapGetters([
            'GET_POEMS',
            'GET_HOST',
            'IS_LOADED'
        ]),
        isLoad(){
            return this.IS_LOADED
        },
        getHostCaptcha(){
            let host = this.GET_HOST
             return host.replace('/api','')
        },
        listPoems(){
            return this.GET_POEMS
        },
    },
    watch:{
        nameId(){
            document.getElementById('main-content-single-id').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
                })
            this.refreshPage()
        }
    },
    mounted() {
        this.refreshPage()
        this.windowArt()
        document.getElementById('main-content-single-id').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
                })
        this.customKeyWords = document.querySelector('meta[name="Keywords"]').content
        document.querySelector('meta[name="Keywords"]').content = this.listPoems.key_words
    },
    updated() {
        document.querySelector("title").innerHTML = this.GET_POEMS.title
        document.querySelector('meta[name="Keywords"]').content = this.listPoems.key_words
    },
    beforeUnmount() {
        document.querySelector('meta[name="Keywords"]').content = this.customKeyWords
    },
}
</script>

<style lang="scss">
.load-spin{
    margin-left: 139px;
    margin-top: 21px;
}
.popup-art_bk{
	background:rgba(0,0,0,0.3);
	position:fixed;
	z-index:1;
	top: 0;
	left: 0;
	bottom: 0;
	right: 0;
	width: auto;
  height: auto;
}
.btn-wrp{
    display: flex;
    justify-content: right;
}
.commentDel{
    margin-top: 14px;
    margin-right: 13px;
    font-size: .9em;
    border: none;
    background-color: #e0dbd4;
         border-bottom: 1px solid transparent;
         color: #323232;
    &:hover{
        cursor: pointer;
         border-bottom: 1px solid #161616;
         color: #161616;
    }
}

.popup-art {
	position: fixed;
	z-index:2;
	left: 50%;
	top: 50%;
	transform: translate(-50%,-50%);
	width: 77%;
    height: 77%;
    background-size: contain;
    background-repeat: no-repeat;
}

.popup-art {
  pointer-events: none;
}
main{
        .main-content-single{
            width: 412px;
            margin-left: 98px;
            margin-top: 24px;

            &-comment{
                padding-top: 52px;
                width: 379px;
                .result{
                    margin-right: 15px;
                    padding: 11px;
                }
                .commentAuthor{
                    .commentAuthorName{
                        display: flex;
                        
                        i{
                            margin-right: 13px;
                            font-size: 2em;
                        }
                        p{
                            padding-top: 8px;
                        }
                    }
                    .commentAuthorText{
                        position: relative;
                        margin: 23px auto;
                        padding: 10px;
                        width: 87%;
                        min-height: 10px;
                        background: rgb(224, 219, 212);
                        border: 1px solid rgb(162, 162, 162);

                        &::before{
                            content: '';
                            position: absolute;
                            top: -20px;
                            left: 17px;
                            border: 10px solid #e9e4dc;
                            border-bottom: 10px solid rgb(162, 162, 162);
                            border-left: 10px solid rgb(162, 162, 162);
                            z-index: 0;
                        }
                        &::after {
                            content: '';
                            position: absolute;
                            top: -18px;
                            left: 18px;
                            border: 10px solid transparent;
                            border-bottom: 10px solid #e0dbd4;
                            border-left: 10px solid #e0dbd4;
                            z-index: 1;
                        }
                    }
                }
                .commentform{
                    .captch-wrp{
                            display: inline;
                    }
                    .formcommtext{
                        background: transparent;
                        resize: none;
                        width: 96%;
                        box-sizing: border-box;
                        outline: none;
                        margin-bottom: 14px;
                        border: 1px solid #a2a2a2;
                        &:focus, &:hover{
                            border: 1px solid #646060;
                        }
                    }
                    .captcha{}
                    #id_captcha_1 {
                        border: none;
                        border-bottom: 1px solid #a2a2a2;
                        background: transparent;
                        height: 20px;
                        outline: none;
                        margin-right: 37px;
                        width: 87px;
                        &:focus, &:hover{
                            border-bottom: 1px solid #646060;
                        }
                    }
                    .commentform-wrp{
                        display: flex;
                        padding-top: 23px;
                        justify-content: space-between;
                        padding-right: 20px;
                    }
                    .formcommauthor{
                        border: none;
                        border-bottom: 1px solid #a2a2a2;
                        background: transparent;
                        width: 150px;
                        height: 20px;
                        outline: none;
                        &:focus, &:hover{
                            border-bottom: 1px solid #646060;
                        }
                    }
                    .formcommemail{
                        border: none;
                        border-bottom: 1px solid #a2a2a2;
                        background: transparent;
                        width: 150px;
                        height: 20px;
                        outline: none;
                        display: block;
                        margin-left: 35px;
                        &:focus, &:hover{
                            border-bottom: 1px solid #646060;
                        }
                        
                    }
                    .input-submit-mess{
                        margin-top: 35px;
                        margin-left: 215px;
                        background-color: #ebe6e0;
                        border: 1px solid #a2a2a2;
                        padding: 11px;
                        margin-right: 15px;
                        &:hover{
                            cursor: pointer;
                            border: 1px solid #646060;
                        }
                        i{
                            margin-left: 12px;
                            font-size: 18px;
                        }
                    }
                }
            }

            &-item{
                padding-left: 24px;
                &>p{
                    padding: 15px;
                }
                &-info{
                    display: flex;
                    color: #686c4a;
                    font-size: .8em;
                    padding-left: 27px;
                    padding-bottom: 8px;
                    p{
                        padding-left: 5px;
                        padding-right: 15px;
                    }
                }
                h1{
                    color: #686c4a;
                    font-size: 1.3em;
                    padding-bottom: 9px;
                }
                &-img{
                        height: 212px;
                        width: 354px;
                        box-sizing: border-box;
                        position: relative;
                        display: flex;
                        justify-content: center;
                         background-color: #f0f0f0;

                         &:hover{
                             cursor: pointer;
                         }

                        border: 2px solid #91919144;
                    padding: 6px;
                    border-block-color: #4494;
                    box-shadow: 0px 2px 2px #818181;

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