<template>
	<div class="table-search-container">
		<el-form ref="searchFormRef" :model="state.form" size="default" class="table-search-form" @submit.prevent>
			<el-form-item v-for="item in search" :key="item.prop" :label="item.label" class="table-search-item">
				<el-input
					v-if="item.type === 'input'"
					v-model="state.form[item.prop]"
					:placeholder="item.placeholder"
					clearable
					class="table-search-input"
				/>
				<el-date-picker
					v-else-if="item.type === 'date'"
					v-model="state.form[item.prop]"
					type="date"
					:placeholder="item.placeholder"
					clearable
					class="table-search-input"
				/>
				<el-date-picker
					v-else-if="item.type === 'daterange'"
					v-model="state.form[item.prop]"
					type="daterange"
					range-separator="To"
					:start-placeholder="item.startPlaceholder || 'Start date'"
					:end-placeholder="item.endPlaceholder || 'End date'"
					clearable
					class="table-search-range"
				/>
				<el-select v-else-if="item.type === 'select'" v-model="state.form[item.prop]" :placeholder="item.placeholder" clearable class="table-search-input">
					<el-option v-for="option in item.options || []" :key="option.value" :label="option.label" :value="option.value" />
				</el-select>
			</el-form-item>
			<el-form-item class="table-search-actions">
				<el-button type="primary" @click="onSearch">查询</el-button>
				<slot name="actions" />
			</el-form-item>
		</el-form>
	</div>
</template>

<script setup lang="ts" name="tableSearch">
import { reactive, ref, watch } from 'vue';
import type { FormInstance } from 'element-plus';

const props = defineProps({
	search: {
		type: Array as () => TableSearchType[],
		default: () => [],
	},
});

const emit = defineEmits(['search']);

const searchFormRef = ref<FormInstance>();
const state = reactive({ form: {} as EmptyObjectType });

const initForm = () => {
	props.search.forEach((item) => {
		if (state.form[item.prop] === undefined) state.form[item.prop] = item.type === 'daterange' ? [] : '';
	});
};

const onSearch = () => {
	initForm();
	emit('search', { ...state.form });
};

watch(() => props.search, initForm, { immediate: true, deep: true });
</script>

<style scoped lang="scss">
.table-search-container {
	width: 100%;
	.table-search-form {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0;
	}
	.table-search-item {
		margin-right: 28px;
		margin-bottom: 15px;
		:deep(.el-form-item__label) {
			padding-right: 12px;
		}
	}
	.table-search-input {
		width: 180px;
	}
	.table-search-range {
		width: 280px;
	}
	.table-search-actions {
		margin-bottom: 15px;
	}
}
</style>
