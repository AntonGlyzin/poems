<template>
    <div  class='main-content-win'>
            <img class="starmen" src="../../assets/images/starmen.png" alt="orange tree" />
            <div class="carousel">
                <label @click="nextPic('prev')" class="prev fa fa-arrow-circle-left"  aria-hidden="true"></label>
                <label @click="nextPic('next')" class="next fa fa-arrow-circle-right"  aria-hidden="true"></label>
            <!-- images from unsplash.com -->
                <img class="img-carousel" src="../../assets/images/photo_2022-04-10_13-51-50.jpg"  />
                <img class="img-carousel" src="../../assets/images/photo_2022-04-10_13-52-14.jpg"  />
            </div>
            <img class="img-pismo" src="../../assets/images/photo_2022-04-10_13-54-32.jpg"  />
    </div>
</template>

<script>
import $ from 'jquery';
import {mapGetters} from 'vuex'
export default {
    name: 'win-page',
    data() {
        return {
            opacity:1,
            blockX:0,
            customKeyWords:''
        }
    },
    methods: {
        
        windowArt(){
            $('.img-carousel').click(function(){
                let src = $(this).attr('src')
                $("body").append("<div class='popup'>"+ 
						 "<div class='popup_bg'></div>"+ 
						 "<img src='"+src+"' class='popup_img' />"+ 
						 "</div>");
                $(".popup").fadeIn(200);
                $(".popup_bg").click(function(){	
                    $(".popup").fadeOut(200);	
                    setTimeout(function() {	
                            $(".popup").remove(); 
                            }, 200);
                });
            })
        },
        nextPic(v){
            if(this.blockX){
                document.getElementsByClassName('img-carousel')[0].style = `transform: translate(-400px, 0px);`
                document.getElementsByClassName('img-carousel')[1].style = `transform: translate(-400px, 0px);`
                document.getElementsByClassName('prev')[0].style = `display: none;`
                document.getElementsByClassName('next')[0].style = `display: block;`
                this.blockX = 0
            }else{
                document.getElementsByClassName('img-carousel')[0].style = `transform: translate(0px, 0px);`
                document.getElementsByClassName('img-carousel')[1].style = `transform: translate(0px, 0px);`
                document.getElementsByClassName('next')[0].style = `display: none;`
                document.getElementsByClassName('prev')[0].style = `display: block;`
                this.blockX = 1
            }
        }
    },
    computed:{
        ...mapGetters([
            'GET_HOST',
        ]),
    },
    mounted() {
        document.querySelector("title").innerHTML = 'Стихи - «Любовь за гранью звёзд»'
        this.windowArt()

        this.customKeyWords = document.querySelector('meta[name="Keywords"]').content
        document.querySelector('meta[name="Keywords"]').content = 'поэт года стихи медаль федор достоевский 200 стихотворения любовь философские номинант премия перо писатель награда'
    },
    beforeUnmount() {
        document.querySelector('meta[name="Keywords"]').content = this.customKeyWords
    },
}
</script>

<style lang="scss">
.img-carousel:hover{
    cursor: pointer;
}
.popup {
	position: absolute;
	height:100%;
	width:100%;
	top:0;
	left:0;
	display:none;
	text-align:center;
}

.popup_bg {
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


.popup_img {
	position: fixed;
	z-index:2;
	left: 50%;
	top: 50%;
	transform: translate(-50%,-50%);
	width: 90%;
}

.popup_img {
  pointer-events: none;
}
.img-pismo{
    width: 398px;

  box-sizing: border-box;
  box-shadow:
   0 1px 4px rgba(0, 0, 0, .3),
   -23px 0 20px -23px rgba(0, 0, 0, .8),
   23px 0 20px -23px rgba(0, 0, 0, .8),
   0 0 40px rgba(0, 0, 0, .1) inset;

}
.starmen{
    width: 300px;
    margin-left: 50px;
    margin-top: -30px;
}
.main-content-win{
    width: 398px;
    margin-left: 102px;
    margin-top: 55px;
}
.carousel {
    display: flex;
    overflow: hidden;
    position: relative;

    width: 100%;
  max-width: 550px;
  box-sizing: border-box;
  padding: 14px;
  box-shadow:
   inset 0 0 100px hsla(0,0%,0%,.2),
   inset 0px 1px 5px #999,
   inset 0px 2px 0px #888,
   inset 0px 3px 0px #777,
   inset 0px 4px 0px #666,
   inset 0px 5px 0px #555,
   inset 0px 6px 0px #444,
   inset 0px 7px 0px #333,
   inset 0px 8px 7px #001135;

    @mixin strelka{
        font-size: 44px;
    position: absolute;
    z-index: 1;
    top: 122px;
    color: #878787;
    &:hover{
            cursor: pointer;
            color: #ababab;
        }

    }
    .prev{
        @include strelka;
    left: 5px;
    display: none;
    }

    .next{
       @include strelka;
    left: 351px;
    
    }
    
    img {
        width: 100%;
        transform: translate(-400px, 0px);
        transition: all 500ms;
    }
}


</style>