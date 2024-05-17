<template>
  <GoogleMap :api-key="apiKey" style="width: 100%; height: 500px" :center="center" :zoom="15">
    <Marker :options="{ position: center }" />
  </GoogleMap>
</template>

<script setup>
import { GoogleMap, Marker } from 'vue3-google-map'

const center = { lat: 40.689247, lng: -74.044502 }
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
</script>
