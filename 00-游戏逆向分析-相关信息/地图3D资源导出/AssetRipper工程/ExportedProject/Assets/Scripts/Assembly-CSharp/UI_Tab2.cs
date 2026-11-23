using UnityEngine;
using UnityEngine.UI;

public class UI_Tab2 : MonoBehaviour
{
	[SerializeField]
	private Image tabImage;

	[SerializeField]
	private Sprite[] tabSprites;

	[SerializeField]
	private GameObject[] buttons;

	private int curTabIndex;

	public void ChangeTab(int index)
	{
	}
}
