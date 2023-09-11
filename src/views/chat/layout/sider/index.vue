<script setup lang='ts'>
import type { CSSProperties } from 'vue'
import { computed, ref, watch } from 'vue'
import { NButton, NLayoutSider } from 'naive-ui'
import List from './List.vue'
import { useAppStore, useChatStore } from '@/store'
import { useBasicLayout } from '@/hooks/useBasicLayout'
import { PromptStore } from '@/components/common'
import beimingLogo from '@/assets/beiming-logo.png'

const appStore = useAppStore()
const chatStore = useChatStore()
const { isMobile } = useBasicLayout()
const show = ref(false)
const collapsed = computed(() => appStore.siderCollapsed)
function handleAdd() {
  chatStore.addHistory({ title: '新对话', uuid: Date.now(), isEdit: false })
  if (isMobile.value)
    appStore.setSiderCollapsed(true)
}
function handleUpdateCollapsed() {
  appStore.setSiderCollapsed(!collapsed.value)
}
const getMobileClass = computed<CSSProperties>(() => {
  if (isMobile.value) {
    return {
      position: 'fixed',
      zIndex: 50,
    }
  }
  return {}
})
const mobileSafeArea = computed(() => {
  if (isMobile.value) {
    return {
      paddingBottom: 'env(safe-area-inset-bottom)',
    }
  }
  return {}
})
watch(
  isMobile,
  (val) => {
    appStore.setSiderCollapsed(val)
  },
  {
    immediate: true,
    flush: 'post',
  },
)
</script>

<template>
  <NLayoutSider
    :collapsed="collapsed"
    :collapsed-width="0"
    :width="260"
    :show-trigger="isMobile ? false : 'arrow-circle'"
    collapse-mode="transform"
    position="absolute"
    bordered
    :style="getMobileClass"
    @update-collapsed="handleUpdateCollapsed"
  >
    <div class="flex flex-col h-full left-background" :style="mobileSafeArea">
      <main class="flex flex-col flex-1 min-h-0">
        <div class="beiming-logo">
          <img :src="beimingLogo">
        </div>

        <div class="p-4">
          <NButton :focusable="false" color="#ffffff" ghost dashed block @click="handleAdd">
            {{ $t('chat.newChatButton') }}
          </NButton>
        </div>
        <div class="flex-1 min-h-0 pb-4 overflow-hidden">
          <List />
        </div>
        <div class="p-4">
          <NButton :focusable="false" block @click="show = true">
            {{ $t('store.siderButton') }}
          </NButton>
        </div>
      </main>
      <!-- <Footer /> -->
      <div class="beiming-footer">
        <span>北明软件 · GPT</span>
        <span>BEIMING SOFTWARE · GPT</span>
      </div>
    </div>
  </NLayoutSider>
  <template v-if="isMobile">
    <div v-show="!collapsed" class="fixed inset-0 z-40 bg-black/40" @click="handleUpdateCollapsed" />
  </template>
  <PromptStore v-model:visible="show" />
</template>

<style scoped>
.left-background {
  background: linear-gradient(161deg,#1a90cd 0%, #63dc66 100%);
  border: 1px solid rgba(0,0,0,0.10);
  box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.10), 0px 0px 12px 0px rgba(0,0,0,0.25);
}
.beiming-logo{
  width: 92px;
  height: 26px;
  margin-top:24px;
  margin-left: 26px;
}
.beiming-logo img{
  width: 100%;
  height: 100%;
}
.beiming-footer{
  display: flex;
  flex-direction: column;
  margin-bottom: 17px;
  margin-left: 26px;

}
.beiming-footer span:nth-child(1){
  /* background: #ffffff; */
  font-size: 16px;
  font-family: Source Han Sans, Source Han Sans-700;
  font-weight: 700;
  text-align: LEFT;
  color: #ffffff;
  line-height: 16px;
}
.beiming-footer span:nth-child(2){
  /* background: #ffffff; */
  font-size: 10px;
  font-family: Source Han Sans, Source Han Sans-500;
  font-weight: 500;
  text-align: LEFT;
  color: #ffffff;
  line-height: 16px;
  margin-top: 4px;
}
</style>
