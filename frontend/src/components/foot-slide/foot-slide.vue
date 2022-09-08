<template>
    <div class="slider">
        <div class="slide"  v-for="slide in slidePoems" :key="slide.slug"><img :src="slide.photo" />
        <p @click="goToPoem(slide.slug)">{{slide.title}}</p></div>
        
    </div>
</template>

<script>
import {mapGetters} from 'vuex'
import axios from "axios"
export default {
    name: 'foot-slide',
    props: {},
    data(){
        return{
            slidePoems:[]
        }
    },
    components: {
    },
    methods: {
        createSlider(){
                var slider = document.querySelector('.slider');
            var sliders = slider.children;
    
    
    
    
            var initX = null;  
            var transX = 0;
            var rotZ = 0;
            var transY = 0;
        
            var curSlide = null;
            
            var Z_DIS = 50;
            var Y_DIS = 10;
            var TRANS_DUR = 0.4;
    
            var images=document.querySelectorAll('img');
            for(var i=0;i<images.length;i++)
            {
                images[i].onmousemove=function(e){
                    e.preventDefault()
                    
                }
                images[i].ondragstart=function(e){
                    return false;
                    
                }
            }
    
            function init() {
            
                var z = 0, y = 0;

                for (var i = sliders.length-1; i >=0; i--) {
                    sliders[i].style.transform = 'translateZ(' + z + 'px) translateY(' + y + 'px)';
                
                    z -= Z_DIS;
                    y += Y_DIS;
                }


                attachEvents(sliders[sliders.length - 1]);

            
            
            }
            function attachEvents(elem) {
                curSlide = elem;

                curSlide.addEventListener('mousedown', slideMouseDown, false);
                curSlide.addEventListener('touchstart', slideMouseDown, false);
            }
            init();
            function slideMouseDown(e) {
            
                if (e.touches) {
                    initX = e.touches[0].clientX;
                }
                else {
                    initX = e.pageX;
                }
            
            
                document.addEventListener('mousemove', slideMouseMove, false);
                document.addEventListener('touchmove', slideMouseMove, false);

                document.addEventListener('mouseup', slideMouseUp, false);
                document.addEventListener('touchend', slideMouseUp, false);
            }
            var prevSlide = null;
    
            function slideMouseMove(e) {
                var mouseX;
            
                if (e.touches) {
                    mouseX = e.touches[0].clientX;
                }
                else {
                    mouseX = e.pageX;
                }

                transX += mouseX - initX;
                rotZ = transX / 20;

                transY = -Math.abs(transX / 15);
            
            
            
                curSlide.style.transition = 'none';
                curSlide.style.webkitTransform = 'translateX(' + transX + 'px)' + ' rotateZ(' + rotZ + 'deg)' + ' translateY(' + transY + 'px)';
            curSlide.style.transform = 'translateX(' + transX + 'px)' + ' rotateZ(' + rotZ + 'deg)' + ' translateY(' + transY + 'px)';
                var j = 1;
                //remains elements
                for (var i = sliders.length -2; i >= 0; i--) {

                sliders[i].style.webkitTransform = 'translateX(' + transX/(2*j) + 'px)' + ' rotateZ(' + rotZ/(2*j) + 'deg)' + ' translateY(' + (Y_DIS*j) + 'px)'+ ' translateZ(' + (-Z_DIS*j) + 'px)';
                sliders[i].style.transform = 'translateX(' + transX/(2*j) + 'px)' + ' rotateZ(' + rotZ/(2*j) + 'deg)' + ' translateY(' + (Y_DIS*j) + 'px)'+ ' translateZ(' + (-Z_DIS*j) + 'px)';
                sliders[i].style.transition = 'none';
                j++;
                }      
                
                
                
                initX =mouseX;
                e.preventDefault();
                if (Math.abs(transX) >= curSlide.offsetWidth-30) {
                
                    document.removeEventListener('mousemove', slideMouseMove, false);
                    document.removeEventListener('touchmove', slideMouseMove, false);
                    curSlide.style.transition = 'ease 0.2s';
                    curSlide.style.opacity = 0;
                    prevSlide = curSlide;
                    attachEvents(sliders[sliders.length - 2]);
                    slideMouseUp();
                    setTimeout(function () {
                        
                    
                        
                    
                        
                        slider.insertBefore(prevSlide, slider.firstChild);
                        
                        prevSlide.style.transition = 'none';
                        prevSlide.style.opacity = '1';
                        slideMouseUp();
                        
                    },201);
                    
                    
                    
                    return;
                }
            }
            function slideMouseUp() {
                transX = 0;
                rotZ = 0;
                transY = 0;
            
                curSlide.style.transition = 'cubic-bezier(0,1.95,.49,.73) '+TRANS_DUR+'s';

                curSlide.style.webkitTransform = 'translateX(' + transX + 'px)' + 'rotateZ(' + rotZ + 'deg)' + ' translateY(' + transY + 'px)';
            curSlide.style.transform = 'translateX(' + transX + 'px)' + 'rotateZ(' + rotZ + 'deg)' + ' translateY(' + transY + 'px)';
                //remains elements
                var j = 1;
                for (var i = sliders.length -  2; i >= 0; i--) {
                    sliders[i].style.transition = 'cubic-bezier(0,1.95,.49,.73) ' + TRANS_DUR / (j + 0.9) + 's';
                sliders[i].style.webkitTransform = 'translateX(' + transX + 'px)' + 'rotateZ(' + rotZ + 'deg)' + ' translateY(' + (Y_DIS*j) + 'px)' + ' translateZ(' + (-Z_DIS*j) + 'px)';
                sliders[i].style.transform = 'translateX(' + transX + 'px)' + 'rotateZ(' + rotZ + 'deg)' + ' translateY(' + (Y_DIS*j) + 'px)' + ' translateZ(' + (-Z_DIS*j) + 'px)';

                j++;
                }
                
                document.removeEventListener('mousemove', slideMouseMove, false);
                document.removeEventListener('touchmove', slideMouseMove, false);
            
            }
        },
        goToPoem(url){
            this.$router.push(`/poems/poem/${url}`)
        },
        getPoemsSlide(url) {
        return axios(this.GET_HOST+url, {
          method: "GET"
        })
          .then((slidePoems) => {
              this.slidePoems = slidePoems.data
              setTimeout(this.createSlider, 1000);
          })
          .catch((error) => {
            console.log(error)
            return error;
          })
      },
    },
    computed:{
        ...mapGetters([
            'GET_POEMS_SLIDE',
            'GET_HOST'
        ]),
        poemSlide(){
            return this.GET_POEMS_SLIDE
        }
    },
    mounted() {
        
        let url = '/poems/slide/8/'
        this.getPoemsSlide(url)
        
        
    },
}
</script>

<style lang="scss">

@-webkit-keyframes animation{from{opacity:0; -webkit-transform:scale(1.2) rotateX(45deg);transform:scale(1.2) rotateX(45deg);} to{ }}

@-webkit-keyframes animation2{from{opacity:0; -webkit-transform:scale(1.2) rotateX(45deg);transform:scale(1.2) rotateX(45deg);} to{ }}



.slider div p{
    color:#1c1c1c;
    bottom: -31px;
    padding: 5px;
    font-size: 1.4em;
    &:hover{
        cursor: pointer;
        color: #4c4c4c;
    }
}
.slider{

     -webkit-animation:animation ease 1s;animation-delay:.8s;animation-fill-mode:backwards;
 

        margin:60px auto 0 auto;
        height:360px;
        width:240px;
        padding:40px;
        top:100px;

        perspective:1000px;
        transition:ease-in-out .2s;
             /*-webkit-transform:rotateX(45deg);
             -webkit-transform-style:preserve-3d;
                 position:absolute;*/
}



.slide img { text-align:center;
max-width: 100%;
    max-height: 100%;
-webkit-user-drag:none;
user-drag:none;
-moz-user-drag:none; 
border-radius:2px; }


.slide{
    &:hover{
        cursor: grab;
    }
    

      -webkit-user-select:none;
user-select:none;
  -moz-user-select:none;
    position:absolute;
        height:280px;
    width:240px;

box-shadow: 0px 10px 30px 0px rgba(0,0,0,0.14);
background:#fcfcfc;
             -webkit-transform-style:preserve-3d;
              transform-style:preserve-3d;
  -moz-transform-style:preserve-3d;
             text-align:center;
             /*overflow:hidden;*/
             border:12px white solid;
             box-sizing:border-box;
             border-bottom:55px white solid;
             border-radius:5px;


    
}
.transition {
     -webkit-transition: cubic-bezier(0,1.95,.49,.73) .4s ;
   -moz-transition: cubic-bezier(0,1.95,.49,.73) .4s ;
      transition: cubic-bezier(0,1.95,.49,.73) .4s ;
}





</style>