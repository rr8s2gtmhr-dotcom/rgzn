<template>
	<div class="railway-page layout-padding">
		<div class="railway-page-content layout-padding-view layout-padding-auto">
			<TableSearch :search="state.tableData.search" @search="onSearch">
				<template #actions>
					<el-button type="success" @click="onExport">导出</el-button>
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

<script setup lang="ts" name="railwayDetection">
import { defineAsyncComponent, reactive, ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { useBusinessCrud } from '/@/utils/businessCrud';

const Table = defineAsyncComponent(() => import('/@/components/table/index.vue'));
const TableSearch = defineAsyncComponent(() => import('/@/components/tableSearch/index.vue'));
const CrudDialog = defineAsyncComponent(() => import('/@/components/crudDialog/index.vue'));

const crud = useBusinessCrud('detections');
const tableRef = ref<RefType>();
const state = reactive<BusinessTableState & { dialogVisible: boolean; dialogTitle: string; editing: EmptyObjectType; fields: CrudField[] }>({
	dialogVisible: false,
	dialogTitle: '',
	editing: {},
	fields: [
		{ key: 'relarderNo', label: '减速顶编号', required: true },
		{ key: 'trackNo', label: '股道号' },
		{ key: 'installHeight', label: '安装高度(mm)' },
		{ key: 'fastPressure', label: '快压力值(Kp)' },
		{ key: 'slowPressure', label: '慢压力值(Kp)' },
		{ key: 'returnTime', label: '回程时间(秒)' },
		{ key: 'gapWidth', label: '间隙宽度(mm)' },
		{ key: 'frontImage', label: '正面图地址' },
		{ key: 'testTime', label: '测试时间' },
		{ key: 'detector', label: '检测人员' },
	],
	tableData: {
		data: [],
		header: [
			{ key: 'relarderNo', colWidth: '130', title: '减速顶编号', type: 'text', width: '', isCheck: true },
			{ key: 'installHeight', colWidth: '120', title: '安装高度(mm)', type: 'text', width: '', isCheck: true },
			{ key: 'fastPressure', colWidth: '120', title: '快压力值(Kp)', type: 'text', width: '', isCheck: true },
			{ key: 'slowPressure', colWidth: '120', title: '慢压力值(Kp)', type: 'text', width: '', isCheck: true },
			{ key: 'returnTime', colWidth: '130', title: '回程时间(秒)', type: 'text', width: '', isCheck: true },
			{ key: 'gapWidth', colWidth: '130', title: '间隙宽度(mm)', type: 'text', width: '', isCheck: true },
			{ key: 'frontImage', colWidth: '100', title: '正面图', type: 'image', width: '70', height: '40', isCheck: true },
			{ key: 'testTime', colWidth: '160', title: '测试时间', type: 'text', width: '', isCheck: true },
			{ key: 'detector', colWidth: '', title: '检测人员', type: 'text', width: '', isCheck: false },
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
			{ label: '站段', prop: 'trackNo', placeholder: '请输入股道', required: false, type: 'input' },
			{
				label: '检测时间',
				prop: 'detectTime',
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
	state.dialogTitle = '新增检测记录';
	state.dialogVisible = true;
};
const onEditRow = (row: EmptyObjectType) => {
	state.editing = { ...row };
	state.dialogTitle = '修改检测记录';
	state.dialogVisible = true;
};
const onDialogSubmit = async (form: EmptyObjectType) => {
	await crud.submit(form);
	getTableData();
};
const onExport = () => ElMessage.success('检测数据导出已触发');
const onDelRow = async (row: EmptyObjectType) => {
	try {
		await crud.remove(row, `检测记录 ${row.relarderNo}`);
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
