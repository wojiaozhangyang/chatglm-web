<script lang="ts" setup>
import { computed } from 'vue'
import { NAvatar } from 'naive-ui'
import { useUserStore } from '@/store'
import { isString } from '@/utils/is'

interface Props {
  image?: boolean
}
defineProps<Props>()

const userStore = useUserStore()

const avatar = computed(() => userStore.userInfo.avatar)
</script>

<template>
  <template v-if="image">
    <NAvatar v-if="isString(avatar) && avatar.length > 0" :src="avatar" />
    <NAvatar v-else round />
  </template>
  <span v-else class="text-[28px] dark:text-white">
    <svg id="Layer_1" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="40px" height="40px" viewBox="0 0 40 40" enable-background="new 0 0 40 40" xml:space="preserve">  <image
      id="image0" width="40" height="40" x="0" y="0"
      href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAMAAAC7IEhfAAAABGdBTUEAALGPC/xhBQAAACBjSFJN
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABL1BMVEUAAAD/////////////
////////////////////////////////////////////////////////////////////////////
///q8f3J3PvX5fz8/f+mxvhWk/JTkfJwpPTn7/250vluovTP4PtgmfO+1vqGsfbc6PxYlPKGsvbZ
5/x7q/VemPOZvvf5/P+ewfff6vz3+v6xzfmbwPjJ3fv6+/5+rPW0z/n0+P681Pq50vrv9f7U4/xo
n/Pk7v3R4vvy9v6ryfmWvPdroPR4qfXO4PupyPikxPiTuvfs8/6ewfiDsPWBrvVzpvRmnfPB1/p2
p/Tf6v36/P+DsPacv/eIs/akxfi20PnE2fusyvnM3vuhw/iUuvfG2/vx9v7p8f3h7Pxjm/P5+/5x
pPSuy/mQj7pZAAAAF3RSTlMABDh7r9fvPCSL5yAYm/v3l1/rXAi3YLD7+ykAAAABYktHRAH/Ai3e
AAAAB3RJTUUH5wgOBiQtp4B8CQAAAfdJREFUOMt9lXtb2jAUxgO0hSKFDpGjIhFdFeecEy9jog7F
yxzW6zadblOnfv/PYEJpmtMmO3/0Sd/n9yTtm5M3hMiVSmcM0wKwTCOTTRFd5ew8SJW3R5RYwSlC
rEpuIcm9sUBR5dEYVnFAU24FcWOgrbGKlhufmKypSRdxU3VKpxuS4ITcKOJmKK9Zec7q0JcyAqcH
IH0rSVZBsTB4ATgH8cVHShicD8CmrBVzDLRjdjQXOPcOizbrg3wMhMX39aUPy1jLp0hW4fHHlYSU
Jplw2FpdW9eDGWIMRxuf2Je1ZfDzZmdLgAYxh6Nt/gueBG7tsPcvIWiSsLu6HKwHU2zvssceF3rC
cxKOavvclIPDcdg46nztABxjlwQI3/onqzVo9ed9enpGe/7A+E4EJhp78A10oQHnF6ftaLvFz4ia
CLawhVVT2CNqLpjxEqtGZHhQV9+PftB9j/aPf3o7TdnwtBjvXt90/U3WsL/Ob+8AflP6JwKzUlMw
P/zgBDT4B07WpX9mTRG1WY/Sv/IWNqQdt3mQhAFxP3Wja4rSIFwSZ7/tXTxgxQ0OV8zzR+aOj5Ty
MIKqGDxk4D+kiADCiz89U/qSXFgRKU93Tfn1P+EDOo6Rro5zEMcDqKzCrKoimt1SHCs6imjm4RIP
+5z2Xkhlo+sjja+PV4bnh0fc2owYAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIzLTA4LTE0VDA2OjM2
OjQ1KzAwOjAwjbm5NQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMy0wOC0xNFQwNjozNjo0NSswMDow
MPzkAYkAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjMtMDgtMTRUMDY6MzY6NDUrMDA6MDCr8SBW
AAAAAElFTkSuQmCC"
    />
    </svg>

  </span>
</template>
