using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class HUD_BagButton : MonoBehaviour, IPointerEnterHandler, IEventSystemHandler, IPointerDownHandler
{
	public int bagIndex;

	public Sprite normalSprite;

	public Sprite focusSprite;

	public Image image;

	public void ChangeNormalImage()
	{
	}

	public void ChangeFocusImage()
	{
	}

	public void OnPointerEnter(PointerEventData eventData)
	{
	}

	public void OnPointerDown(PointerEventData eventData)
	{
	}
}
