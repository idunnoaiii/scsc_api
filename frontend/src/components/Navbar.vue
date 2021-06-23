<template >
    <nav>
        <v-navigation-drawer  v-model="drawer" light app class="white darken-3 py-0 elevation-4">
            <v-container>
                <v-row>
                    <v-col md="9">
                        <v-progress-circular 
                        :rotate="300"
                        :size=50
                        :value="value"
                        class="mt-n1"
                        >
                            {{value}}
                        </v-progress-circular>
                    </v-col>
                    <v-col md="3">
                        <v-icon right class="mt-1">
                            fas fa-bars
                        </v-icon>
                    </v-col>
                </v-row>
            </v-container>
        </v-navigation-drawer>
    </nav>
</template>


<script>
export default {
    data: function(){
        return {
            drawer: true,
            interval: {},
            value:0
        }
    },
    beforeDestroy(){
        clearInterval(this.interval)
    },
    mounted(){
        this.interval = setInterval(() => {
            if(this.value === 100)
                return (this.value = 0)
            this.value += 10
        }, 1000);
    }
}
</script>
