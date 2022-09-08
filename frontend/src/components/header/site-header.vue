<template>
    <header>
        <div class="contain">
            <h1>Стихи</h1> 
            <h2>от автора</h2> 
            <div class="search-poems" >
                <input type="text" name="" v-model="search" placeholder="Поиск среди звёзд..."> 
                <svg class="img" xmlns="http://www.w3.org/2000/svg" version="1.0" width="34.000000pt" height="34.000000pt" viewBox="0 0 64.000000 64.000000" preserveAspectRatio="xMidYMid meet">
                <g transform="translate(0.000000,64.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none">
                <path d="M410 557 c-74 -59 -131 -127 -105 -127 11 0 157 113 161 125 3 8 4 21 2 29 -2 12 -16 6 -58 -27z"/>
                <path d="M525 534 c-95 -48 -215 -123 -215 -135 0 -25 -22 -3 -41 41 -25 59 -55 73 -99 46 -19 -10 -52 -16 -97 -16 -76 -1 -70 -10 19 -29 52 -11 57 -15 72 -52 9 -22 16 -46 16 -55 0 -23 35 -86 62 -111 12 -12 48 -33 79 -48 31 -14 85 -50 120 -80 94 -81 110 -73 46 23 -29 43 -60 96 -71 119 l-18 41 57 57 c48 49 165 210 165 229 0 13 -28 4 -95 -30z m-305 -72 c0 -13 -12 -22 -22 -16 -10 6 -1 24 13 24 5 0 9 -4 9 -8z"/>
                </g>
                </svg>
            </div>
        </div>
        <div class="head-astron"></div>
        <div class="head-stars"></div>
    </header>
</template>

<script>
import {mapActions} from 'vuex'
export default {
    name: 'site-header',
    data() {
        return {
            search:'',
        }
    },
    methods: {
        ...mapActions([
        'GET_POEMS_FROM_API'
        ]),
    },
    watch:{
        search(v){
            if(v.length){
                this.$router.push(`/poems/search/${v}`)
            }else{
                this.$router.push(`/poems/`)
            }
            
        }
    }
}
</script>
<style lang='scss'>

</style>