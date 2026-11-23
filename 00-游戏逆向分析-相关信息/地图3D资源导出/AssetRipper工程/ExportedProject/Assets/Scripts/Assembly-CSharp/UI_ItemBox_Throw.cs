using UnityEngine;
using UnityEngine.UI;

public class UI_ItemBox_Throw : MonoBehaviour
{
	[SerializeField]
	private RawImage itemBox;

	[SerializeField]
	private RawImage[] itemIcons;

	[SerializeField]
	private Button[] itemBtns;

	public ItemObject item { get; private set; }

	public void BindItem(int slot, ItemObject item)
	{
	}
}
