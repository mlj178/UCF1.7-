using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI_ItemPanel : MonoBehaviour
{
	[SerializeField]
	private GameObject itemBoxPrefab;

	[SerializeField]
	private int maxCount;

	[SerializeField]
	private Scrollbar scrollbar;

	[SerializeField]
	private Vector4 scrollArea;

	private List<UI_ItemBox> boxList;

	private int curPage;

	private int totalPageCount;

	private float scrollValuePerPage;

	private List<ItemObject> list;

	public Action<UI_ItemBox> updateBoxFunc;

	private void Update()
	{
	}

	public void Init(Action<UI_ItemBox> btnFunc)
	{
	}

	public void SetItems(List<ItemObject> newList)
	{
	}

	public void OnScrollBarValueChange(float value)
	{
	}

	private void JumpToItemPage(int pageID)
	{
	}

	public void UpdateAllItemBox()
	{
	}
}
