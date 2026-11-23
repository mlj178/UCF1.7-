using UnityEngine;
using UnityEngine.UI;

public class HUD_ProjectionSign : RecyclableObject
{
	[SerializeField]
	protected Image image;

	[SerializeField]
	private RectTransform rect;

	[SerializeField]
	private Text distanceText;

	protected Transform bindTransform;

	[SerializeField]
	private Vector3 offset;

	[SerializeField]
	private float showRange;

	protected virtual void Update()
	{
	}

	protected virtual void SetGraphVisible(bool visible)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	protected virtual bool GetVisible()
	{
		return false;
	}

	public virtual void Bind(Transform bind)
	{
	}

	public void SetSprtie(Sprite spr)
	{
	}
}
