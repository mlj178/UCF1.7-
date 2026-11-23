using UnityEngine;
using UnityEngine.UI;

public class HUD_Nano4T_AttributeIcon : MonoBehaviour
{
	[SerializeField]
	private bool isNano;

	private RectTransform rect;

	private Image image;

	private Text description;

	private static readonly Vector2 Pos_Nano;

	private static readonly Vector2 Pos_Center;

	private static readonly Vector2 Pos_Soldier;

	public Nano4T_Attribute attribute { get; private set; }

	public bool isActive => false;

	public void Init()
	{
	}

	public void UpdatePosition(bool isCenter)
	{
	}

	public void SetActive(bool active)
	{
	}

	public void BindAttribute(Nano4T_Attribute attribute)
	{
	}

	public void UpdateDescription(bool withName)
	{
	}
}
