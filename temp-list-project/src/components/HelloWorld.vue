<template>
  <v-container>
        <v-card>
          <v-list two-line subheader v-if="tempList">
            <v-subheader>General</v-subheader>

            <v-list-tile avatar v-for="obj in tempList" :key="obj._id">
              <v-list-tile-content v-if="obj.hasOwnProperty('ds18b20')">
                <v-list-tile-title>DS18B20 <span>{{ formatTime(obj.timestamp) }}</span> </v-list-tile-title>
                <v-list-tile-sub-title>temperature: {{ obj.ds18b20.temperature }} </v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-content v-if="obj.hasOwnProperty('dht11')">
                <v-list-tile-title>DHT11 <span>{{ formatTime(obj.timestamp) }}</span> </v-list-tile-title>
                <v-list-tile-sub-title>Temperature: {{ obj.dht11.temperature }} | Humidity: {{ obj.dht11.humidity }}</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>

          </v-list>
        </v-card>
  </v-container>
</template>

<script>
import moment from "moment";
export default {
  data: () => ({
    tempList: null
  }),
  mounted() {
    this.axios.get("/sensor/temp/8").then(({ data }) => {
      this.tempList = data;
    });
  },
  mqtt: {
    "KevinFan/lab305/update"(data) {
      this.tempList = [JSON.parse(data), ...this.tempList];
    }
  },
  methods: {
    formatTime(stamp) {
      console.log(stamp);
      return moment(new Date(stamp)).format("YYYYMMDD, HH:mm:ss");
    }
  }
};
</script>

<style>
</style>
