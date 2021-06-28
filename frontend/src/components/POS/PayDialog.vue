<template>
  <v-dialog v-model="enableDialog" max-width="500px">
    <v-card>
      <v-card-title class="text-center text-h5">
        <v-spacer></v-spacer>
        Payment
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card>
        <v-row class="ma-3">
          <v-col>
            <v-row class="pl-5">
              <v-col class="pa-1" cols="3" align-self="center">
                <span> Price $ </span>
              </v-col>
              <v-col class="pa-1" cols="9">
                <input
                  class="input pa-2"
                  v-model="priceAmount"
                  type="text"
                  disabled
                />
              </v-col>
            </v-row>

            <v-row class="pl-5">
              <v-col class="pa-1" cols="3" align-self="center">
                Payment $
              </v-col>
              <v-col class="pa-1" cols="9">
                <input class="input pa-2" v-model="paymentAmount" type="text" />
              </v-col>
            </v-row>

            <v-row>
              <v-spacer></v-spacer>
              <v-col class="text-align-center min-width-300">
                <v-row
                  class="mx-auto"
                  v-for="item in calculatorRows"
                  :key="item[0]"
                >
                  <v-col
                    class="pa-2 mx-auto"
                    v-for="number in item"
                    :key="number"
                    max-width="100px"
                  >
                    <v-btn class="mx-auto" color="green">
                      {{ number }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="2">
                <v-btn color="red"> AC </v-btn>
              </v-col>
              <v-spacer></v-spacer>
            </v-row>
          </v-col>
        </v-row>
      </v-card>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" @click="$emit('close-delete')">
          <span class="text-white"> Change $ </span>
        </v-btn>
        <v-btn color="#5fbeaa" @click="$emit('delete-item-confirm')">
          <span class="text-white"> Confirm Payment </span>
        </v-btn>
        <v-btn color="red darken-1" @click="$emit('close-delete')">
          <span class="text-white"> Cancel </span>
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "PayDialog",
  data: function () {
    return {
      calculatorRows: [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [-1, 0, -2],
      ],
      paymentAmount: 0,
      priceAmount: 123.0,
      enableDialog:true,
    };
  },
  methods: {},
};
</script>


<style scoped>
.min-width-300 {
  min-width: 300px !important;
}
.text-white {
  color: #ffffff !important;
}
</style>