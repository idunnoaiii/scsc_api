<template>
  <v-row justify="center">
    <v-dialog v-model="$store.state.addCustomerDialog" max-width="640px">
      <v-card>
        <v-card-title>
          <span class="text-h5">New Customer</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" lazy-validation v-model="valid">
            <v-container>
              <v-row>
                <v-col cols="12" sm="6" md="12">
                  <v-text-field
                    label="Phone*"
                    v-model="newCustomer.contact"
                    :rules="[required('Phone'), isPhone(), isAlrealdyExist()]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="12">
                  <v-text-field
                    label="Name"
                    v-model="newCustomer.name"
                    :rules="[required('Name')]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="12">
                  <v-text-field
                    label="Address"
                    v-model="newCustomer.address"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
          <small>*indicates required field</small>
        </v-card-text>
        <v-divider class="mb-4"></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary darken-1"
            class="white--text"
            text
            @click="$store.commit('SET_ADD_CUSTOMER', false)"
          >
            Cancel
          </v-btn>
          <v-btn
            color="green darken-1"
            class="white--text"
            @click="addNewCustomer"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import axios from "../axios";
import { mapState } from "vuex";

export default {
  data: function () {
    return {
      valid: true,
      newCustomer: {
        name: "",
        contact: "",
        address: "",
      },
      required(inputName) {
        return (v) =>
          (v && v.toString().length > 0) || `${inputName} is required.`;
      },
      isPhone() {
        let re = /(0[3|5|7|8|9])+([0-9]{8})\b/;
        return (v) => (v && re.test(v)) || `Not a valid phone number.`;
      },
      isAlrealdyExist() {
        let self = this;
        return (v) =>
          (v && !self.customers.some((c) => c.text.split(" - ")[1] == v)) ||
          "This customer phone is already existed!";
      },
    };
  },
  methods: {
    addNewCustomer() {
      let self = this;
      if (!this.$refs.form.validate()) {
        return;
      }

      axios
        .post("/api/v1/customers", {
          name: self.newCustomer.name,
          contact: self.newCustomer.contact,
          address: self.newCustomer.address,
        })
        .then((response) => {
          if (response.status == 200 && response.data) {
            this.$store.commit("SET_TOAST", {
              toastMsg: "Customer added!",
              toastColor: "green",
            });
            this.$store.dispatch('POS/addCusomterInPOS', response.data.id);
          }
        })
        .catch((error) => {
          console.error(error);
        });

      this.$refs.form.reset();
      this.$store.commit("SET_ADD_CUSTOMER", false);
    },
  },
  computed: {
    ...mapState("POS", {
      customers: "customers",
    }),
  },
};
</script>