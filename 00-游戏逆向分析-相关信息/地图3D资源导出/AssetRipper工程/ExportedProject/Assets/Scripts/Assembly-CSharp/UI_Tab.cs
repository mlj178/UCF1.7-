using UnityEngine;
using UnityEngine.Events;

public class UI_Tab : MonoBehaviour
{
	[SerializeField]
	private GameObject[] tabs;

	[SerializeField]
	private GameObject[] buttons;

	private int curTabIndex;

	public UnityEvent<int> OnValueChange;

	public void ChangeTab(int index)
	{
	}
}
