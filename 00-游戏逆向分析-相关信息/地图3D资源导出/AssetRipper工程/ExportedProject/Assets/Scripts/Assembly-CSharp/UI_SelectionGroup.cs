using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

public class UI_SelectionGroup : MonoBehaviour
{
	[SerializeField]
	private Button[] buttons;

	public UnityEvent<int> OnValueChange;

	public int currentSelection { get; private set; }

	public void OnSelectValueChange(int index)
	{
	}
}
