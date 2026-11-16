<template>
	<div class="railway-page layout-padding">
		<div class="railway-page-content layout-padding-view layout-padding-auto">
			<TableSearch :search="state.tableData.search" @search="onSearch">
				<template #actions>
					<el-button type="success" @click="onAdd">新增</el-button>
				</template>
			</TableSearch>
			<Table
				ref="tableRef"
				:data="state.tableData.data"
				:header="state.tableData.header"
				:config="state.tableData.config"
				class="railway-table"
				@delRow="onDelRow"
				@editRow="onEditRow"
				@pageChange="onPageChange"
				@sortHeader="onSortHeader"
			/>
			<CrudDialog v-model="state.dialogVisible" :title="state.dialogTitle" :fields="state.fields" :initial="state.editing" @submit="onDialogSubmit" />
		</div>
	</div>
</template>

<script setup lang="ts" name="railwayMaintain">
import { defineAsyncComponent, reactive, ref, onMounted } from 'vue';
import { useBusinessCrud } from '/@/utils/businessCrud';

const Table = defineAsyncComponent(() => import('/@/components/table/index.vue'));
const TableSearch = defineAsyncComponent(() => import('/@/components/tableSearch/index.vue'));
const CrudDialog = defineAsyncComponent(() => import('/@/components/crudDialog/index.vue'));

const crud = useBusinessCrud('maintains');
const tableRef = ref<RefType>();
const state = reactive<BusinessTableState & { dialogVisible: boolean; dialogTitle: string; editing: EmptyObjectType; fields: CrudField[] }>({
	dialogVisible: false,
	dialogTitle: '',
	editing: {},
	fields: [
		{ key: 'relarderNo', label: '减速顶编号', required: true },
		{ key: 'maintainTime', label: '维修时间', type: 'date' },
		{ key: 'maintainProject', label: '维修项目', required: true },
		{ key: 'maintainUser', label: '维修人员' },
	],
	tableData: {
		data: [],
		header: [
			{ key: 'relarderNo', colWidth: '', title: '减速顶编号', type: 'text', width: '', isCheck: true },
			{ key: 'maintainTime', colWidth: '160', title: '维修时间', type: 'text', width: '', isCheck: true },
			{ key: 'maintainProject', colWidth: '', title: '维修项目', type: 'text', width: '', isCheck: true },
			{ key: 'maintainUser', colWidth: '', title: '维修人员', type: 'text', width: '', isCheck: true },
		],
		config: {
			total: 0,
			loading: false,
			isBorder: false,
			isSelection: false,
			isSerialNo: true,
			isOperate: true,
			isEdit: true,
			disableDeleteConfirm: true,
			enableHeaderColumnSetting: true,
		},
		search: [
			{ label: '编号', prop: 'relarderNo', placeholder: '请输入编号', required: false, type: 'input' },
			{ label: '维修项目', prop: 'maintainProject', placeholder: '请输入维修项目', required: false, type: 'input' },
			{
				label: '维修时间',
				prop: 'maintainTime',
				placeholder: '请选择',
				required: false,
				type: 'daterange',
				startPlaceholder: 'Start date',
				endPlaceholder: 'End date',
			},
		],
		param: { pageNum: 1, pageSize: 10 },
	},
});

const getTableData = async () => {
	state.tableData.loading = true;
	try {
		const { rows, total } = await crud.page(state.tableData.param);
		state.tableData.data = rows;
		state.tableData.config.total = total;
	} finally {
		state.tableData.loading = false;
	}
};
const onSearch = (data: EmptyObjectType) => {
	state.tableData.param = Object.assign({}, state.tableData.param, data);
	tableRef.value?.pageReset();
	getTableData();
};
const onPageChange = (page: TableDemoPageType) => {
	state.tableData.param.pageNum = page.pageNum;
	state.tableData.param.pageSize = page.pageSize;
	getTableData();
};
const onSortHeader = (data: TableHeaderType[]) => {
	state.tableData.header = data;
};
const onAdd = () => {
	state.editing = {};
	state.dialogTitle = '新增维修记录';
	state.dialogVisible = true;
};
const onEditRow = (row: EmptyObjectType) => {
	state.editing = { ...row };
	state.dialogTitle = '修改维修记录';
	state.dialogVisible = true;
};
const onDialogSubmit = async (form: EmptyObjectType) => {
	await crud.submit(form);
	getTableData();
};
const onDelRow = async (row: EmptyObjectType) => {
	try {
		await crud.remove(row, `维修记录 ${row.relarderNo}`);
		getTableData();
	} catch {
		// 用户取消删除
	}
};

onMounted(getTableData);
</script>

<style scoped lang="scss">
.railway-page {
	.railway-page-content {
		padding: 15px;
	}
	.railway-table {
		flex: 1;
		overflow: hidden;
	}
}
</style>
