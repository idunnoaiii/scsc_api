<template>
  <v-layout>
    <v-row justify="center">
      <v-col cols="8">
        <v-data-table
          :headers="headers"
          :items="items"
          sort-by="name"
          class="elevation-1"
          width="90%"
          :search="search"
        >
          <template v-slot:[`item.stock`]="{ item }">
            <span>{{ item.stock == true ? "Yes" : "No" }}</span>
          </template>
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title class="text-h4">Items</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-text-field
                v-model="search"
                label="Search"
                hide-details
                class="mx-4"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    New
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-form ref="form" lazy-validation v-model="valid">
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.name"
                              label="Name*"
                              :rules="[required('Name')]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.description"
                              label="Description"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.price"
                              label="Price*"
                              type="Number"
                              :rules="[required('Price'), minNumberValue(1000)]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" v-if="editedIndex === -1">
                            <v-file-input
                              accept="image/*"
                              label="Image"
                              @change="onFileSelected"
                            ></v-file-input>
                          </v-col>

                          <v-col cols="12" sm="6" md="12">
                            <v-switch
                              v-model="editedItem.stock"
                              :label="`Stock tracking: ${
                                !!editedItem.stock ? 'Yes' : 'No'
                              }`"
                            ></v-switch>
                          </v-col>

                          <v-col cols="12" v-if="editedItem.stock">
                            <v-text-field
                              v-model="editedItem.quantity"
                              label="Quantity*"
                              type="Number"
                              :rules="[required('Quantity'), minNumberValue(0)]"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-form>
                    <small>*indicates required field</small>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="close"
                    >
                      Cancel
                    </v-btn>
                    <v-btn
                      color="green darken-1"
                      class="white--text"
                      @click="save"
                      :disabled="!valid"
                    >
                      Save
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Are you sure you want to delete this item?</v-card-title
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="closeDelete"
                      >Cancel</v-btn
                    >
                    <v-btn
                      color="red darken-1"
                      class="white--text"
                      @click="deleteItemConfirm"
                      >OK</v-btn
                    >
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="load"> Reset </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-layout>
</template>
<script>
import axios from "../../axios";
export default {
  data: () => ({
    valid: true,
    dialog: false,
    password: "",
    search: "",
    dialogDelete: false,
    selectedFile: null,
    stockTracking: false,
    headers: [
      {
        text: "Name",
        align: "start",
        value: "name",
      },
      { text: "Description", value: "description" },
      { text: "Price", value: "price" },
      { text: "Quantity", value: "quantity" },
      { text: "Category", value: "categories" },
      { text: "Stock", value: "stock" },
      { text: "Action", value: "actions", sortable: false },
    ],
    items: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      description: "",
      price: 0,
      expired_date: "",
      image_url: "",
      quantity: 0,
      categories: 0,
      stock: false,
      id: 0,
      is_active: false,
    },
    defaultItem: {
      full_name: "",
      username: "",
      role: "",
    },
    categories: [
      {
        text: "admin",
        value: true,
      },
      {
        text: "user",
        value: false,
      },
    ],
    categorySelected: false,
    required(inputName) {
      return (v) =>
        (v && v.toString().length > 0) || `${inputName} is required.`;
    },
    noSpace() {
      return (v) => (v || "").indexOf(" ") < 0 || "No spaces are allowed";
    },
    minNumberValue(value) {
      return (v) => (v && v >= value) || `Must be greater than ${value}`;
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  // created() {
  //   this.initialize();
  // },

  mounted() {
    this.load();
  },
  methods: {
    load() {
      axios
        .get("api/v1/items/all?skip=0&limit=100")
        .then((response) => {
          this.items = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    onFileSelected(file) {
      this.selectedFile = file;
    },

    editItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.password = "";
    },

    deleteItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      // this.items.splice(this.editedIndex, 1);
      axios
        .delete(`/api/v1/items/${this.editedItem.id}`)
        .then((response) => {
          if (response.status == 200) {
            this.$swal.fire({
              icon: "success",
              title: "Add new item successfully",
            });
            this.load();
          }
        })
        .catch((err) => {
          console.log(err);
        });

      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$refs.form.reset();
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
    //   if (!this.$refs.form.validate()) {
    //     return;
    //   }
      if (this.editedIndex > -1) {
        //update
        Object.assign(this.items[this.editedIndex], this.editedItem);
      } else {
        //add

        const item_added =  {
            name: this.editedItem.name,
            description: this.editedItem.description,
            price: this.editedItem.price,
            quantity: this.editedItem.quantity,
            categories: [],
            stock: this.editedItem.stock,
        }

        let fd = new FormData();

        let item_json = JSON.stringify(item_added)

        fd.append("data", item_json);

        fd.append("image", this.selectedFile, this.selectedFile.name);

        axios.post("/api/v1/items/create", fd).then((response) => {
          console.log(response);
        });

        // axios
        //   .post("/api/v1/items/", this.editedItem)
        //   .then(() => {
        //     this.load();
        //     this.$swal.fire({
        //       icon: "success",
        //       title: "Add new item successfully",
        //     });
        //   })
        //   .catch((err) => {
        //     console.log(err);
        //   });
      }
      this.close();
    },

    filterUser(value, search, items) {
      console.log(items);
      return (
        value != null &&
        search != null &&
        typeof value === "string" &&
        value.toString().indexOf(search) !== -1
      );
    },
  },
};
</script>