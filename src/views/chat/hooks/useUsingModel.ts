import { computed } from 'vue'
import { useMessage } from 'naive-ui'
import { useChatStore } from '@/store'

export function useUsingModel() {
  const ms = useMessage()
  const chatStore = useChatStore()
  const usingModel = computed<String>(() => chatStore.usingModel)

  function toggleUsingModel(model: String) {
    chatStore.setUsingModel(model)
  }

  return {
    usingModel,
    toggleUsingModel,
  }
}
