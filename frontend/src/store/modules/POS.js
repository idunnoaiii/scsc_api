import axios from '../../axios'

const state = () => ({
	orderItems: [],
	customer_checkout: 0,
	totalItem: 0,
	totalPay: 0,
	discount: {
		threshold: 0,
		type: 0,
		value: 0
	},
	checkoutStatus: null,
	showBillDialog: false,
	customers: [],
	customerValue: 0,
})

const getters = {
	totalOrderItem(state) {
		return state.orderItems.reduce((acc, item) => acc + item.quantity, 0)
	},
	totalPrice(state) {
		return state.orderItems.reduce((acc, item) => acc + (item.quantity * item.price), 0)
	},
	discount(state){
		return state.discount;
	}
}

const actions = {
	checkout({ commit, state, getters }, payload) {

		let orderDetail = {
			code: new Date().getTime(),
			user_id: 1,
			status: true,
			tax: 0,
			subtotal: getters.totalPrice - payload.discountValue,
			total: getters.totalPrice,
			discount: payload.discountValue,
			paid: payload.amount,
			change: payload.change,
			order_items: [
				{
					item_id: 0,
					price: 0,
					quantity: 0,
					item_name: "string",
				},
			],
		};

		orderDetail.order_items = state.orderItems.map((item) => ({
			item_id: item.id,
			price: item.price,
			quantity: item.quantity,
			item_name: item.name,
		}));

		axios
			.post("/api/v1/orders/", orderDetail)
			.then(() => {
				commit('SET_CHECKOUT_STATUS', true)
				commit('CLEAR_ORDER_ITEM')
			})
			.catch((err) => {
				console.log(err);
				commit('SET_CHECKOUT_STATUS', false)
			});

	},

	getCustomer({ commit }) {
		axios.get("/api/v1/customers")
			.then((response) => {
				if (response.data) {
					const customers = response.data.map((item) => ({
						text: `${item.phone} - ${item.name}`,
						value: item.phone,
					}));
					customers.unshift({ text: "Walk in customer", value: -1 });
					commit('SET_CUSTOMERS', customers)
				}

			});
	},

	calculateDiscount({getters, commit}) {
		axios.get(`/api/v1/discounts/calculate/${getters.totalPrice}`)
			.then(response => {
				commit("SET_DISCOUNT", response.data)
			})
	}

}

const mutations = {
	ADD_ITEM_TO_ORDER(state, item) {
		let itemIndex = state.orderItems.findIndex(x => x.id == item.id);
		if (itemIndex > -1) {
			state.orderItems[itemIndex].quantity++;
			return
		}
		let orderItem = {
			id: item.id,
			rownumber: state.orderItems.length + 1,
			name: item.name,
			quantity: 1,
			price: item.price,
		};
		state.orderItems.push(orderItem)
	},

	SET_CHECKOUT_STATUS(state, status) {
		state.checkoutStatus = status;
	},

	INCREASE_ITEM_QUANTITY(state, id) {
		let item = state.orderItems.find(x => x.id == id)
		if (item) item.quantity++
	},

	DECREASE_ITEM_QUANTITY(state, id) {
		let item = state.orderItems.find(x => x.id == id)
		if (item == null || item == undefined)
			return;
		if (item.quantity > 1) {
			item.quantity--;
			return;
		}
		state.orderItems = state.orderItems.filter(x => x.id != id);
	},

	CLEAR_ORDER_ITEM(state) {
		state.orderItems = [];
	},

	SET_BILL_DIALOG(state, status) {
		state.showBillDialog = status;
	},


	CLEAR_CHECKOUT_DATA(state) {
		state.orderItems = [];
	},

	DELETE_ITEM_ORDER(state, id) {
		state.orderItems = state.orderItems.filter(x => x.id != id);
	},

	SET_CUSTOMERS(state, payload) {
		state.customers = payload
	},

	SET_DISCOUNT(state, payload) {
		state.discount = payload
	}

}


export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations
}