<template>
    <main>
        <div class='main-top'>
            <blockquote>
                    <p class='main-top-stih' style="padding-left: 10px;">Мироздание пронзила<br>
                                                    Поэтическая сила.<br>
                                                    Век гоняет в венах кровь.<br>
                                                    Ей название - любовь.♡</p></blockquote>

                    
        </div>
            
            <transition name="moveUp">
                <router-view></router-view>
            </transition>
    </main>
</template>

<script>
export default {
    name: 'site-main',
    data() {
        return {
            countComment:0
        }
    },
    components:{
    },
    
}
</script>

<style lang='scss'>
.count-comment{
    margin-left: 122px;
    margin-top: 9px;
}
.moveUp-enter-active{
  animation: moveInUp 300ms ease-in;
}
@keyframes moveInUp{
 0%{
     opacity: 0;
  transform: scale(0.5);
 }
  100%{
  transform: scale(1);;
  opacity: 1;
 }
}
    main .main-top{
        blockquote{
            margin-left: 181px;
            font-size: .8em;
            padding: 20px 6px 6px;
            font-style: italic;
        }
        .rss-me{
            display: flex;
            p{
                font-style: italic;
                font-weight: bold;
                color: #7c805c;
                margin-right: 5px
            }
            a{
                color: #666666;
            }
        }
        &-stih{
            font-size: 1.5em;
            font-family: 'Caveat', cursive;
        }
        
    }
    
    
</style>