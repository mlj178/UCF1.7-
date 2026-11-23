using System;
using UnityEngine;
using UnityEngine.UI;

public class UI_ItemBox : MonoBehaviour
{
	[SerializeField]
	private RawImage itemBox;

	[SerializeField]
	private RawImage itemIcon;

	[SerializeField]
	private Text itemName;

	[SerializeField]
	private Button itemBtn;

	[SerializeField]
	private Text clipBuffText;

	[SerializeField]
	private RawImage categoryImg;

	public int clipBuffCount
	{
		set
		{
		}
	}

	public Texture2D category
	{
		set
		{
		}
	}

	public ItemObject item { get; private set; }

	public void BindItem(ItemObject item)
	{
	}

	public void BindBtnFunction(Action<UI_ItemBox> btnFunc)
	{
	}
}
