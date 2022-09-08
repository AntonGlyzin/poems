<template>
    <footer>
        <div class="footer-wrp-slide">
            <div class="footer-wrp-slide-girl"></div>
            <slide/>
        </div>
        <slideText></slideText>
        <address>
            <p><i style="margin-right: 5px" class="fa fa-copyright" aria-hidden="true"></i>Антон Глызин | <a target="_blank" href="https://vk.com/tosha.glyzin"><i style="margin-right: 5px" class="fa fa-vk" aria-hidden="true"></i>ВКонтакте</a> |
                <a target="_blank" href="https://stihi.ru/avtor/toshaglyzin"><i style="margin-right: 5px" class="fa fa-music" aria-hidden="true"></i>Стихи.ру</a> |
                <a target="_blank" href="https://t.me/tosha_glyzin "><i style="margin-right: 5px" class="fa fa-telegram" aria-hidden="true"></i>Telegram</a></p>
                
        </address>
    </footer>
</template>

<script>
import slide from '../foot-slide/foot-slide.vue'
import slideText from '../slide-text/slide-text'
export default {
    name: 'site-footer',
    components:{
        slide,
        slideText
    },
}
</script>

<style lang="scss">
address{
    font-size: 1.2em;
    margin-left: -88px;
    padding-bottom: 37px;

    a {
        color: #666666;
        text-decoration: none;
    }
    a:hover {
    color: #333333;
}
}

.footer-wrp-slide-girl{
    background: url('../../assets/images/girlmain.png') no-repeat;
    height: 404px;
    position: absolute;
    width: 322px;
    background-size: contain;
    top: 78px;
    left: -123px;
}
.footer-wrp-slide{
    display: flex;
    position: relative;
}
</style>